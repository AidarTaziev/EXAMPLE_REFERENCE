from .auth_methods import auth_logout
from django.shortcuts import HttpResponseRedirect
from django.conf import settings


def sso_login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            local_redirect = request.GET.get('next', '')
            redirect = "http://passport.{0}/auth/?next=http://{1}/{2}" \
                .format(settings.MAIN_DOMAIN, settings.APP_SUBDOMAIN, local_redirect)
        else:
            redirect = '/'

        return HttpResponseRedirect(redirect)


def sso_logout(request):
    if request.method == 'GET':
        return auth_logout(request)
