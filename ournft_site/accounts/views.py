from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .models import Profile
from .forms import ProfileForm

from django.urls import reverse
from ournft_app.forms import CaptchaForm
from ournft_app.models import Image, Notification
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def signup_view(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        form_captcha = CaptchaForm(request.POST)

        if form.is_valid() and form_captcha.is_valid():
            user = form.save()
            Profile(user=user).save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home') 
    else:
        form = UserCreationForm()
        form_captcha = CaptchaForm()
    return render(request, 'signup.html', {'form': form, 'form_captcha':form_captcha})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

class profile_view(TemplateView):
    template_name = "profile.html"


    def dispatch(self, request, *args, **kwargs):
        # if not Profile.objects.filter(user=request.user).exists():
        #     return redirect('edit_profile')
        context = {
            'selected_user': request.user,
            # 'notifications' : Notification.objects.filter(user=request.user)
            'notifications' : request.user.notifications.all()
        }
        return render(request, self.template_name, context)

class EditProfileView(TemplateView):
    template_name = "edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        context = {
            'form': form,
            'images': Image.public.filter(owner=request.user)
        }
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                # messages.success(request, u'Profile updated')
                return redirect('accounts:profile')
        return render(request, self.template_name, context)

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None

@login_required(login_url='home')
def SetAvatar(request, image_hash):
    image_obj = get_object_or_404(Image, image_hash=image_hash)
    profile = request.user.profile
    if profile.avatar==image_obj:
        profile.avatar=None
        profile.save()
    elif image_obj.owner == profile.user and image_obj.visibility == True:
        profile.avatar = image_obj
        profile.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
