from django.shortcuts import redirect
from django.urls import reverse
from .models import Profile

class ProfileCreationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user)
                return redirect(reverse('profile_edit'))
        return None