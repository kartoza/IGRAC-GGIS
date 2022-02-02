from django.conf import settings
from allauth.account.views import SignupView
from core.forms.signup import SignupWithNameForm


class CustomSignupView(SignupView):
    form_class = SignupWithNameForm

    def get_context_data(self, **kwargs):
        ret = super(CustomSignupView, self).get_context_data(**kwargs)
        ret.update({'account_geonode_local_signup': settings.SOCIALACCOUNT_WITH_GEONODE_LOCAL_SINGUP})
        return ret
