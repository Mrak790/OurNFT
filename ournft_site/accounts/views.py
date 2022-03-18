from django.shortcuts import render, redirect

# Create your views here.

from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .models import Profile
from .forms import ProfileForm

from django.urls import reverse

def signup_view(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

class profile_view(TemplateView):
    template_name = "accounts/profile.html"


    def dispatch(self, request, *args, **kwargs):
        # if not Profile.objects.filter(user=request.user).exists():
        #     return redirect('edit_profile')
        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)

class EditProfileView(TemplateView):
    template_name = "accounts/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                # messages.success(request, u'Profile updated')
                return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None