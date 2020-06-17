from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import render

from apps.access.models import InvitedEmail


class ClosedAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        print("Checking for signup!")
        return False


class InvitedSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        u = sociallogin.user
        print("Checking for social permission!!: {}".format(u.email))
        if InvitedEmail.objects.filter(address__iexact=u.email).exists():
            return True
        return False

    def pre_social_login(self, request, sociallogin):
        if not self.is_open_for_signup(request, sociallogin):
            raise ImmediateHttpResponse(render(request, "account/signup_closed.html",))
