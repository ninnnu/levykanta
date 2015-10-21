def header(request):
    stuff = dict()
    if request.user.is_authenticated():
        stuff['user'] = request.user
    else:
        stuff['user'] = None
    return stuff

