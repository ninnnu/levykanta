# -*- coding: UTF-8 -*-

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.template import Context, loader, RequestContext
from discdb.models import Disc, DiscForm, NewDiscForm, TrackForm, Owner, Track, Wish, WishForm
from django.db.models import Q # OR-queries
# from discdb.forms import NewDiscForm, DiscForm, TrackForm, BarcodeForm, WishForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings
# from barcode import Barcode, NotFound

import simplejson
import MySQLdb # Discogs

# Create your views here.
def index(request):
    cd_list = Disc.objects.filter(returned = False).order_by("artist")
    c = { 'cd_list': cd_list }
    return render_to_response('discdb/index.html', c, context_instance=RequestContext(request))

def show(request, cd_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    debug = ""
    try:
        cd = Disc.objects.get(pk=cd_id)
    except:
        raise Http404

    tracks = []
    for track in cd.tracks.all():
        tracks.append(track)

    tmpl = loader.get_template('discdb/details.html')
    c = { 'cd': cd, 
          'tracks': tracks }
        
    return render_to_response('discdb/details.html', c, context_instance=RequestContext(request))

def show_by_author(request, author_id):
    cd_list = Disc.objects.filter(owner = author_id, returned = False).order_by("artist")
    # c = { 'cd_list': cd_list }
    c = { 'cd_list': cd_list }
    return render_to_response('discdb/index.html', c, context_instance=RequestContext(request))

def add_disc(request):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/discdb/")
    c = {}
    if request.method == "POST":
        data = request.POST.copy()
        data['owner'] = find_owner(data['owner'])
        form = NewDiscForm(data)
        if form.is_valid():
            cd = form.save()
            
            owner = Owner.objects.get(pk=data['owner'])
            owner.discs.add(cd)
            owner.save()
            
            for track_id in data['track_ids'].split(","):
                if(track_id == ''):
                    continue
                try:
                    cd.tracks.add(track_id)
                except:
                    continue
                t = Track.objects.get(id = track_id)
                t.disc = cd
                t.save()
            c['added'] = "Added CD"
            data['artist'] = None
            data['barcode'] = None
            data['name'] = None
            data['track_ids'] = None
            data['owner'] = request.POST['owner']
            form = NewDiscForm(data)
    else:
        form = NewDiscForm()
    c['discform'] = form
    c.update(csrf(request))
    return render_to_response('discdb/add.html', c, context_instance=RequestContext(request))

@csrf_exempt
def suggest(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    db = MySQLdb.connect(settings.DISCOGS_SERVER, settings.DISCOGS_USERNAME, settings.DISCOGS_PASSWORD, settings.DISCOGS_DATABASE)
    dbc = db.cursor()
    inp = request.POST['input']
    
    if(inp.isdigit() and len(inp) >= 8):
        results = dbc.execute("SELECT id, artist, title FROM discogs WHERE barcode = %s GROUP BY artist, title", (inp,))
    else:
        results = dbc.execute("SELECT id, artist, title FROM discogs WHERE MATCH(artist, title) AGAINST (%s IN BOOLEAN MODE) GROUP BY artist, title", (request.POST['input'],)) 
    
    freeCD = False

    if(results > 1000):
        return HttpResponse(simplejson.dumps([{'value': -1, 'label': "Liikaa tuloksia"}]))
    if(results == 0):  # Plan B: Try FreeCD
        freeCD = True
        dbc.execute("SELECT cd_id, artist, title FROM freecd WHERE MATCH(artist, title) AGAINST(%s IN BOOLEAN MODE) GROUP BY artist, title", (request.POST['input'],))

    row = dbc.fetchone()
    results = []
    while(row):
        if(freeCD == True):
            results.append({'value': "f_"+str(row[0]), 'label': "%s - %s" % (row[1], row[2])})
        else:
            results.append({'value': row[0], 'label': "%s - %s" % (row[1], row[2])})

        row = dbc.fetchone()
    results.append({'value':0, 'label': u"Lisää oma"})
    return HttpResponse(simplejson.dumps(results))

@csrf_exempt
def suggest_cataloged(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    inp = request.POST['input']
    if(inp.isdigit() and len(inp) >= 8):
        results_raw = Disc.get(barcode = inp, returned = False)
    else:
        results_raw = Disc.objects.filter(artist__icontains = inp, returned = False)
    results = []
    for r in results_raw:
        results.append({'value':r.id, 'label': "%s - %s" % (r.artist, r.name)})
    return HttpResponse(simplejson.dumps(results))

def edit_disc(request, cd_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    cd = Disc.objects.get(pk = cd_id)
    form = DiscForm(instance = cd)
    c = Context({ 'form': form })
    return render_to_response('discdb/edit.html', c, context_instance=RequestContext(request))

def lookup_cdid(request, cd_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    db = MySQLdb.connect(settings.DISCOGS_SERVER, settings.DISCOGS_USERNAME, settings.DISCOGS_PASSWORD, settings.DISCOGS_DATABASE)
    dbc = db.cursor()
    
    if(cd_id[0] == "f"):
        freeCD = True
        cd_id = cd_id[2:]
        dbc.execute("SELECT artist, title, 0 FROM freecd WHERE cd_id = %s", (cd_id,))
    else:
        freeCD = False
        dbc.execute("SELECT artist, title, barcode FROM discogs WHERE id = %s", (cd_id,))
    cd = dbc.fetchone()
    
    tracks = []
    if(freeCD == True):
        dbc.execute("SELECT artist, title FROM freetracks WHERE disc = %s", (cd_id,))
    else:
        dbc.execute("SELECT artist, title FROM discogs_tracks WHERE cd_id = %s", (cd_id,))
    row = dbc.fetchone()
    while(row):
        tracks.append({'artist': row[0], 'title': row[1]})
        row = dbc.fetchone()
    entry = {'artist': cd[0], 'title': cd[1], 'barcode': cd[2], 'tracks': tracks}
    return HttpResponse(simplejson.dumps(entry))

def lookup_code(request, barcode):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    barcode = Barcode(barcode)
    try:
        barcode.lookup()
    except NotFound:
        return HttpResponse('{"error": "NotFound"}')
    return HttpResponse(barcode.json())

def lookup_catalogue(request, cd_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    cd = Disc.objects.get(pk = cd_id)
    return HttpResponse(simplejson.dumps({'id': cd_id, 'artist': cd.artist, 'name': cd.name, 'owner': cd.owner.name}))

def add_track(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    if request.method == "POST":
        track = TrackForm(request.POST)
        if(track.is_valid()):
            track = track.save()
            return HttpResponse(track.pk)
        else:
            return HttpResponse('{"error": "Form not valid"}')
    else:
        return HttpResponse('{"error": "Use POST"}')

def find_owner(formname):
    try:
        owner = Owner.objects.get(name = formname)
    except:
        owner = Owner()
        owner.name = formname
        owner.save()
    return owner.pk

def login_view(request):
    c = {}
    if(request.method == "POST"):
        username = request.POST['username']
        pw = request.POST['pw']
        user = authenticate(username=username, password = pw)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/discdb/')
            else:             
                pass # Disabled account
        else:
            pass # Invalid login
        c['error'] = "Login failed"
    c.update(csrf(request))
    return render_to_response("discdb/login.html", c, context_instance=RequestContext(request))

def search_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    c = {}
    if(request.method == "POST"):
        # Results-format: [{'name': name, 'url': url}]
        results = []
        
        if('track' in request.POST):
            res = Track.objects.filter(Q(name__icontains = request.POST['track']) | Q(artist__icontains = request.POST['track']))
            for r in res:
                try:
                    name = r.artist+" - "+r.name+" ("+r.disc.name+")"
                except:
                    pass
                url = "/discdb/show/"+str(r.disc.pk)+"/"
                results.append({'name': name, 'url': url})
        
        elif('artist' in request.POST):
            res = Disc.objects.filter(artist__icontains = request.POST['artist'])
            for r in res:
                name = r.artist+" - "+r.name
                url = "/discdb/show/"+str(r.pk)+"/"
                results.append({'name': name, 'url': url})

        elif('disc' in request.POST):
            res = Disc.objects.filter(name__icontains = request.POST['disc'])
            for r in res:
                name = r.artist+" - "+r.name
                url = "/discdb/show/"+str(r.pk)+"/"            
                results.append({'name': name, 'url': url})
        c['results'] = results

    return render_to_response("discdb/search.html", c, context_instance=RequestContext(request))

def wish(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    # TODO: Stub
    c = {}
    if(request.method == "POST"):
        data = request.POST.copy()
        if('wishsource' not in data):
           data['source'] = request.META['REMOTE_ADDR']
        form = WishForm(data)
        if(form.is_valid()):
            c['added'] = True
            form.save()
    else:
        form = WishForm
    c['wishform'] = form
    return render_to_response("discdb/toivo.html", c, context_instance=RequestContext(request))

def show_wishes(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    # TODO: Login-check
    c = {}
    c['granted'] = list()
    c['not_granted'] = list()
    for wish in Wish.objects.all():
        if(wish.track.find(" - ") > 0):
            wish.discs = list()
            artist = wish.track.split(" - ")[0]
            track = wish.track.split(" - ")[1]
            tracks = Track.objects.filter(artist__icontains = artist, name__icontains = track)
            print tracks
            for match in tracks:
                try:
                    wish.discs.append(match.disc)
                    print match.disc.name
                except:
                    continue
        else:
            wish.discs = list()
            tracks = Track.objects.filter(name__icontains = wish.track)
            for match in tracks:
                try:
                    wish.discs.append(match.disc)
                except:
                    continue
           
        if(wish.done == True):
            c['granted'].append(wish)
        else:
            c['not_granted'].append(wish)
    c.update(csrf(request))
    return render_to_response("discdb/toiveet.html", c, context_instance=RequestContext(request))

def grant_wish(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    # TODO: Logincheck
    if(request.method == "POST"):
        wishid = request.POST['wishid']
        wish = Wish.objects.get(pk = wishid)
        wish.done = True
        wish.save()
    return show_wishes(request)

def return_disc(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/discdb/")
    c = {}
    if(request.method == "POST"):
        if(request.POST['barcode']):
            d = Disc.objects.get(id = request.POST['barcode'])
            d.returned = True
            d.save()
            c['returned'] = True
    return render_to_response("discdb/return.html", c, context_instance=RequestContext(request))
