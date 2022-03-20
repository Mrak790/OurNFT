from email.mime import image
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ImageForm, RestoreImageForm
from .models import Image, GetImageHash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.timezone import make_aware

@login_required(login_url='home')
def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj, 'is_unique': form.instance.is_unique})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})





@login_required(login_url='home')
def image_restore_view(request):
    """Process images uploaded by users"""
    context = {}
    if request.method == 'POST':
        try:
            form = RestoreImageForm(request.POST, request.FILES)
            if form.is_valid():
                obj=Image.objects.get(image_hash=GetImageHash(form.files['image']),secret=form.data['secret'])
                obj.owner = request.user
                obj.datetime = make_aware(datetime.now())
                obj.save(is_creating=False)
                context = {
                    'accepted': True,
                    'image' : obj.image,
                    'asked' : True,
                    'form' : form
                }
                return render(request, 'restore.html', context)
            else:
                print('invalid form')
                print(form.errors)
        except ObjectDoesNotExist:
            print("Wrong image or secret")

        context = {
                'accepted': False,
                'asked' : True,
                'form' : form
            }    
        return render(request, 'restore.html', context)
    else:
        form = RestoreImageForm()
        context = {
            'asked' : False,
            'form' : form
        }
        return render(request, 'restore.html', context)


from django.views.generic import TemplateView

class home(TemplateView):      
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        context = {
            'images': Image.public.all()
        }
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.owner = request.user
                is_unique = form.save()
                context['form_obj'] = form.instance
                print("pk: ", form.instance.pk)
                context['is_unique'] = is_unique
                # return redirect('home')
        else:
            form = ImageForm()

        context['form'] = form
        
        return render(request, self.timeline_template_name, context)
