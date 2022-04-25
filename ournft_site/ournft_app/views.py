from dataclasses import field
from django import views
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import View

from .forms import ImageForm, RestoreImageForm, TransferForm, CommentForm, ReportForm, BanUserForm, TokenRestoreForm, ModerTokenRestoreForm
from .models import Image, History, Notification, Comment, Report
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.timezone import make_aware
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
# from django.contrib.auth import get_user_model

# User = get_user_model()

class ImageView(LoginRequiredMixin, TemplateView):
    template_name = 'image.html'

    def get(self, request, *args, **kwargs):
        image_object = get_object_or_404(Image, image_hash=self.kwargs['image_hash'])

        if image_object.visibility==False and image_object.owner!=request.user and not request.user.is_staff:
            return HttpResponseForbidden("Image is private")

        context = {
            'image' : image_object,
            'history' : History.of_image(image_object),
            'comments' : image_object.comments.all(),
            'new_comment' :  CommentForm(),
        }
        return render(request, self.template_name, context)

class ImageRestoreView(LoginRequiredMixin, TemplateView):
    template_name = 'restore.html'

    def get(self, request, *args, **kwargs):
        form = RestoreImageForm()
        context = {
            'asked' : False,
            'form' : form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
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
                return render(request, self.template_name, context)
            
            if obj.owner.profile.avatar == obj:
                obj.owner.profile.avatar = None
                obj.owner.profile.save()
                print("discard avatar")

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
            return render(request, self.template_name, context)


class home(TemplateView):      
    #login_url='home'
    template_name = "home.html"
    timeline_template_name = "timeline.html"
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)
        # print(request.user.get_all_permissions())
        context = {
            'images': Image.most_liked()[:10]
        }
        form = ImageForm()

        context['form'] = form

        return render(request, self.timeline_template_name, context)

    def post(self, request, *args, **kwargs):
        context = {
            'images': Image.most_liked()[:10]
        }
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and not request.user.profile.banned:
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
        context['form'] = form
        
        return render(request, self.timeline_template_name, context)

class ImageLikeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        image_obj = get_object_or_404(Image, image_hash=kwargs.get('image_hash'))

        if image_obj.visibility==False and image_obj.owner!=request.user:
            return HttpResponseForbidden("Image is private")

        if image_obj.likes.contains(request.user):
            image_obj.likes.remove(request.user)
        else:
            image_obj.likes.add(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class ImageTransferView(LoginRequiredMixin,TemplateView):
    template_name = 'transfer.html'
    def get(self, request, *args, **kwargs):
        form = TransferForm(user=request.user)
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TransferForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            obj = form.cleaned_data['image_hash']

            if obj == obj.owner.profile.avatar:
                obj.owner.profile.avatar = None
                obj.owner.profile.save()

            obj.owner = form.cleaned_data['recipient']
            obj.secret = User.objects.make_random_password(length=20)
            obj.save()

            record = History(id=None, datetime= make_aware(datetime.now()), referred_image = obj,  referred_owner = obj.owner)
            record.save()

            obj.notifications.all().delete()
            obj.owner.notifications.create(new_image=obj)

            context = {
                'accepted': True,
                'image' : obj.image,
                'form' : form
            }

            return render(request, self.template_name, context)

        else:
            context = {
                'form' : form
                }    
            return render(request, self.template_name, context)


class GetTransferView(LoginRequiredMixin, TemplateView):
    template_name = 'notification.html'
    def get(self, request, *args, **kwargs):
        notification_obj = get_object_or_404(Notification, id=kwargs.get('id'))
        if notification_obj.user == request.user:
            context = {
                'image' : notification_obj.new_image,
                }
            notification_obj.delete()
            return render(request, 'notification.html', context)
        else:
            return HttpResponseNotFound()

class CommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            image_obj = get_object_or_404(Image, image_hash=kwargs.get('image_hash', None))
            if image_obj.visibility or image_obj.owner==request.user:
                form.instance.image = image_obj
                form.instance.user = request.user
                form.save()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()

class FeedView(ListView):
    model = Image
    template_name = "feed.html"
    context_object_name = 'images'

    def get_queryset(self):
        queryset = {'public_images': Image.public.all(), 
                    'user_images': self.request.user.images.all() if self.request.user.is_authenticated else None,
                    'popular_images': Image.most_liked()[:10]}
        return queryset

class ReportView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class ReportListView(UserPassesTestMixin, ListView):
    model = Report
    template_name = "report_list.html"
    context_object_name = 'reports'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = Report.objects.all()
        return queryset

class DeleteCommentView(UserPassesTestMixin, View):

    def test_func(self):
        print(self.request.user)
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('id'))
        comment.delete()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class BanImageView(UserPassesTestMixin, View):

    def test_func(self):
        print(self.request.user)
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        image = get_object_or_404(Image, image_hash=kwargs.get('image_hash'))
        image.banned = True
        image.visibility = False
        image.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class BanUserView(UserPassesTestMixin, View):

    template_name = 'ban_user.html'

    def test_func(self):
        print(self.request.user)
        return self.request.user.is_staff

    
    def get(self, request, *args, **kwargs):
        form = BanUserForm(user=request.user)
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BanUserForm(request.POST, request.FILES, user = request.user)

        if form.is_valid():
            obj = form.cleaned_data['user']

            obj.profile.banned = not obj.profile.banned
            obj.profile.save()

            context = {
                'accepted': True,
                'username' : obj.username,
                'banned' : obj.profile.banned,
                'form' : form
            }

            return render(request, self.template_name, context)

        else:
            context = {
                'form' : form
                }    
            return render(request, self.template_name, context)


class SwitchVisibleView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        image = get_object_or_404(Image, image_hash=kwargs.get('image_hash', None))

        if request.user == image.owner and image.banned == False:
            image.visibility = not image.visibility
            image.save()
        else: 
            return HttpResponseForbidden()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class TokenRestoreView(LoginRequiredMixin, TemplateView):
    template_name = 'restore.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_staff:
            form = ModerTokenRestoreForm()
        else:
            form = TokenRestoreForm()

        context = {
            'asked' : False,
            'form' : form
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        if request.user.is_staff:
            form = ModerTokenRestoreForm(request.POST, request.FILES)
        else:
            form = TokenRestoreForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                obj=Image.objects.get(image_hash=form.data['image_hash'], secret=form.data['secret'])
            except ObjectDoesNotExist:
                print("Wrong token or secret")
                context = {
                'accepted': False,
                'asked' : True,
                'form' : form
                }    
                return render(request, self.template_name, context)
            
            if obj.owner.profile.avatar == obj:
                obj.owner.profile.avatar = None
                obj.owner.profile.save()
                print("discard avatar")
            
            if request.user.is_staff:
                obj.owner = form.cleaned_data['user']
            else:
                obj.owner = request.user
            obj.secret = User.objects.make_random_password(length=20)
            obj.save()

            record = History(id=None, datetime= make_aware(datetime.now()), referred_image = obj,  referred_owner = obj.owner)
            record.save()

            if request.user.is_staff:
                obj.notifications.all().delete()
                obj.owner.notifications.create(new_image=obj)

            context = {
                'accepted': True,
                'image' : obj.image,
                'secret': obj.secret,
                'asked' : True,
                'form' : form
            }
            return render(request, self.template_name, context)