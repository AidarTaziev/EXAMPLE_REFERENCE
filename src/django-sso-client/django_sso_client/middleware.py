from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import login
from .auth_methods import auth_logout
import requests
from django.apps import apps

User = get_user_model()
try:
    Company = apps.get_model(settings.COMPANY_MODEL)
    CompanyBranch = apps.get_model(settings.COMPANY_BRANCH_MODEL)

except (LookupError, ValueError, AttributeError) as e:
    Company = None
    CompanyBranch = None


try:
    CompanySignatory = apps.get_model(settings.COMPANY_SIGNATORY_MODEL)
except (LookupError, ValueError, AttributeError) as e:
    CompanySignatory = None


class SyncUsersMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if settings.PASSPORT_SESSION_ID_NAME not in request.COOKIES:
            if request.user.is_authenticated:
                return auth_logout(request)
        elif not request.user.is_authenticated:
            passport_user = get_user_from_passport(
                session_id=request.COOKIES[settings.PASSPORT_SESSION_ID_NAME])
            if passport_user:
                local_user = update_or_create_user(passport_user)
                login(request, local_user)
        else:
            passport_user = get_user_from_passport(session_id=request.COOKIES[settings.PASSPORT_SESSION_ID_NAME])
            if passport_user:
                passport_user_id = passport_user.get('user').get('id')
                if request.user.id != passport_user_id:
                    local_user = update_or_create_user(passport_user)
                    login(request, local_user)
            else:
                return auth_logout(request)


def get_user_from_passport(user_id=None, session_id=None):
    data = {
        'session_id': session_id,
        'user_id': user_id,
        'secret': settings.PASSPORT_SECRET_KEY,
    }
    print('pass req data', data)
    try:
        response = requests.post(settings.PASSPORT_USER_CREDENTIALS_URI, data=data)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    print('pass resp data', response.content)

    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            return data['data']
    print(data)
    return None


def update_or_create_user(user_data):
    passport_company = user_data.get('company')
    passport_signatories = user_data.get('signatories')
    user_company = None
    if passport_company and Company:

        default_company_branch = {
            'id': 1,
            'name': 'Полимеры'
        }
        passport_branch = passport_company.get('branch') or default_company_branch
        branch = update_or_create(passport_branch, CompanyBranch)
        passport_company['branch'] = branch
        user_company = update_or_create(passport_company, Company)

        if passport_signatories and CompanySignatory:
            for passport_signatory in passport_signatories:
                update_or_create(CompanySignatory, passport_signatory)

    user = update_or_create(user_data.get('user'), User)
    if Company:
        user.company = user_company
        user.save()

    return user


def update_or_create(data, model):
    pk = data.get('id')
    queryset = model.objects.filter(pk=pk)
    if queryset.exists():
        queryset.update(**data)
        saved_instance = queryset[0]

    else:
        saved_instance = model.objects.create(**data)

    return saved_instance





