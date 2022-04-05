from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.models import User
from .forms import ImageForm, RestoreImageForm, TransferForm
from .models import Image, History, Notification
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.timezone import make_aware
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound, HttpResponseRedirect


def image_view(request, image_hash):
    image = get_object_or_404(Image, image_hash=image_hash)
    if image.visibility or image.owner == request.user:
        history = History.objects.filter(referred_image=image)
        context = {
            'image':image,
            'history':history,
        }
        return render(request, 'image.html', context)
    else :
        return HttpResponseNotFound()


@login_required(login_url='home')
def image_restore_view(request):
    """Process images uploaded by users"""
    context = {}
    if request.method == 'POST':
        form = RestoreImageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=Image.objects.get(image_hash=Image.GetImageHash(form.files['image']),secret=form.data['secret'])
            except ObjectDoesNotExist:
                print("Wrong image or secret")
                context = {
                'accepted': False,
                'asked' : True,
                'form' : form
                }    
                return render(request, 'restore.html', context)
            if obj.owner.avatar == obj:
                obj.owner.avatar = None
            obj.owner = request.user
            obj.secret = User.objects.make_random_password(length=20)
            obj.save()
            record = History(id=None, datetime= make_aware(datetime.now()), referred_image = obj,  referred_owner = obj.owner)
            record.save()
            context = {
                'accepted': True,
                'image' : obj.image,
                'secret': obj.secret,
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



class home(TemplateView):      
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        context = {
            'images': Image.most_liked()[:10]
        }
        
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.owner = request.user
                form.instance.image_hash = Image.GetImageHash(form.instance.image)
                form.instance.secret = User.objects.make_random_password(length=20)
                if Image.IsUnique(form.instance.image_hash):
                    form.save()
                    record = History(id=None, datetime=form.instance.upload_datetime, referred_image = form.instance,  referred_owner = form.instance.owner)
                    record.save()
                    context['form_obj'] = form.instance
                    context['is_unique'] = True
                else:
                    context['form_obj'] = form.instance
                    context['is_unique'] = False
        else:
            form = ImageForm()

        context['form'] = form
        
        return render(request, self.timeline_template_name, context)

@login_required(login_url='home')
def ImageLike(request, image_hash):
    image_obj = get_object_or_404(Image, image_hash=image_hash)
    if image_obj.likes.contains(request.user):
        image_obj.likes.remove(request.user)
    else:
        image_obj.likes.add(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)



@login_required(login_url='home')
def image_transfer_view(request):
    context = {}
    if request.method == 'POST':
        form = TransferForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            
            obj = form.cleaned_data['image_hash']
            obj.owner = form.cleaned_data['recipient']
            obj.secret = User.objects.make_random_password(length=20)
            obj.save()
            record = History(id=None, datetime= make_aware(datetime.now()), referred_image = obj,  referred_owner = obj.owner)
            record.save()
            context = {
                'accepted': True,
                'image' : obj.image,
                'form' : form
            }
            notification = Notification(user=obj.owner, new_image=obj)
            notification.save()
            return render(request, 'transfer.html', context)
        else:
            context = {
                'form' : form
                }    
            return render(request, 'transfer.html', context)
    else:
        print("test")
        form = TransferForm(user=request.user)
        print(request.user.username)
        context = {
            'asked' : False,
            'form' : form
        }
        return render(request, 'transfer.html', context)

@login_required(login_url='home')
def GetTransfer(request, pk):
    notification_obj = get_object_or_404(Notification, pk=pk)
    if notification_obj.user == request.user:
        context = {
        'image' : notification_obj.new_image,
        }
        notification_obj.delete()
        return render(request, 'notification.html', context)
    else:
        return HttpResponseNotFound()