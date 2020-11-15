# Django SSO authentication module for `client app`
**The following fields are required in your settings.py:** 
- **PASSPORT_SESSION_ID_NAME** : session_id key in cookies
- **PASSPORT_SECRET_KEY** : secret key for API 
- **PASSPORT_USER_CREDENTIALS_URI** : API URL for user data receiving 
- **MAIN_DOMAIN** : main domain where your app is located  

**But if you have company model, you should be define following fields:** 
- **COMPANY_MODEL** : string reference to company model with app_label
- **COMPANY_BRANCH_MODEL** : string reference to company branches model 

**Also you should be add urls in your url_patterns:** 
````
urlpatterns = [
    path('test/', views.test),
    path('auth/', include('django_sso_client.urls')),
    path('test2/', views.test2),
]
````
Now you can go on app.domain.com/auth/ and app redirect you on passport.
After success authentication passport will redirect you back on the app.domain.com \
If you need to logout from your account you should be go on app.domain.com/auth/logout.
After that you will be logout on all your apps with this plugin \
\
**Installation**: \
`pip install git+https://github.com/ferma666/sso_auth_module.git`  \

**In requirements.txt** \
`git+https://github.com/ferma666/sso_auth_module.git@releases/tag/v0.0.1#egg=django_sso_client` \
**settings.py example:** 
````
MIDDLEWARE = [
    '........................................................',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_sso_client.middleware.SyncUsersMiddleware',
    '........................................................',
]
# middleware added after Django AuthenticationMiddleware

PASSPORT_SESSION_ID_NAME = 'passport_session_id'
PASSPORT_SECRET_KEY = 'secret'
MAIN_DOMAIN = 'kartli.ch'
APP_SUBDOMAIN = 'auction.{0}'.format(MAIN_DOMAIN)
PASSPORT_USER_CREDENTIALS_URI  = 'https://passport.{0}/auth/data'.format(MAIN_DOMAIN)

# IF THE APP HAVE A COMPANY MODEL
COMPANY_MODEL = 'company.Company'
COMPANY_BRANCH_MODEL = 'company.OrganizationBranch'
#TODO: complete the guide
````



