from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        user = request.user
        
        # agar user ka role set nahi hai
        if not hasattr(user, 'role') or user.role is None:
            return reverse('choose_role')
        
        # role ke hisaab se redirect
        if user.role == 'driver':
            return '/trips/dashboard/'
        else:
            return '/accounts/passenger_dashboard/'