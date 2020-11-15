from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from sprav import views as sprav_views


urlpatterns = [
    url(r'^admin_panel/', admin.site.urls),
    url(r'^bank_account/', include('bank_account.urls')),
    url(r'^polymer/', include('sprav.urls')),
    url('', sprav_views.search, name='sprav'),
]

if settings.LOCAL_SETTINGS:
    urlpatterns.insert(0, url('auth/', include('authentication.urls')))
else:
    urlpatterns.insert(0, url('auth/', include('src.django-sso-client.django_sso_client.urls'))
)

