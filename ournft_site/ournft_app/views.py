#<<<<<<< likes
from django.shortcuts import render, reverse
from django.views.generic import ListView,DetailView
from .models import *
from taggit.models import Tag
from django.http import HttpResponseRedirect
# Create your views here.
class TagMixin(object):
          def get_context_data(self, **kwargs):
              context = super(TagMixin, self).get_context_data(**kwargs)
              context['tags'] = Tag.objects.all()
              return context

class PostIndexView(TagMixin,ListView):
    model = Blog
    template_name = 'blog.html'
    queryset=Blog.objects.all()
    context_object_name = 'posts'

class TagIndexView(TagMixin,ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PostDetailView(DetailView):
    model = Blog
    context_object_name = 'post'
    template_name = 'blog-detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # adding like count
        like_status = False
        ip = get_client_ip(request)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status = True
        else:
            like_status=False
        context['like_status'] = like_status


        return self.render_to_response(context)


def postLike(request, pk):
    post_id = request.POST.get('blog-id')
    post = Blog.objects.get(pk=post_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
#=======
from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import ImageForm, RestoreImageForm
from .models import Image, History
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.timezone import make_aware
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound

def image_view(request, image_hash):
    image = get_object_or_404(Image, image_hash=image_hash)
    if image.visibility or image.owner == request.user:
        context = {
            'image':image
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
            obj.owner = request.user
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
            'images': Image.public.all()
        }
        
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.owner = request.user
                form.instance.image_hash = Image.GetImageHash(form.instance.image)
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
#>>>>>>> main
