from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common = Group.objects.get(name='common')
        common.user_set.add(user)
        return user


class BasicSocialSignupForm(SocialSignupForm):
    def save(self, request):
        user = super(BasicSocialSignupForm, self).save(request)
        common = Group.objects.get(name='common')
        common.user_set.add(user)
        return user