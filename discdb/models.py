from django.db import models
from django import forms
    
# Create your models here.
class Disc(models.Model):
    artist = models.CharField("Artisti", max_length = 100)
    name = models.CharField("Levyn nimi", max_length = 100)
    owner = models.ForeignKey('Owner', related_name='owners', unique=False)
    returned = models.BooleanField("Palautettu")
    barcode = models.CharField("Viivakoodi", max_length = 16, blank=True)
    tracks = models.ManyToManyField('Track', related_name='tracks', db_table="Discs_to_Tracks", blank = True)
    def __unicode__(self):
      return unicode(self.artist+" - "+self.name)

class Owner(models.Model):
    name = models.CharField("Nimi", max_length = 100)
    discs = models.ManyToManyField(Disc, related_name="discs", blank = True)
    def __unicode__(self):
      return self.name

class Track(models.Model):
    artist = models.CharField("Artisti", max_length = 100)
    name = models.CharField("Kappaleen nimi", max_length = 100)
    disc = models.ForeignKey(Disc, unique = False, default = 1, blank = True, null = True)
    def __unicode__(self):
      return unicode(self.artist+" - "+self.name)

class Wish(models.Model):
    source = models.CharField("Toivoja", max_length= 100)
    track = models.CharField("Toive", max_length = 254)
    done = models.BooleanField("Toteutettu", default = False)
    def __unicode__(self):
        return unicode(self.source+": "+self.track)

class NewDiscForm(forms.ModelForm):
    class Meta:
        model = Disc
        #fields = ('owner', 'barcode')
        exclude = ('returned', 'tracks')
        widgets = {
            'owner': forms.TextInput(),
            'name': forms.TextInput(attrs={'readonly': 'yes'}),
            'artist': forms.TextInput(attrs={'readonly': 'yes'})
        }

class DiscForm(forms.ModelForm):
    class Meta:
        model = Disc

class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Disc
        fields = ('barcode',)

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('artist', 'name')

class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        exclude = ('done',)
