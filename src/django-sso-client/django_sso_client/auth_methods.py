from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.conf import settings


def auth_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    if settings.MAIN_DOMAIN:
        cookie_domain = ".{0}".format(settings.MAIN_DOMAIN)
    else:
        cookie_domain = ".kartli.ch"

    response.delete_cookie(settings.PASSPORT_SESSION_ID_NAME, domain=cookie_domain)
    return response
