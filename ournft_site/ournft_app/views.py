from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ImageForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin')
def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = User.objects.get(id=request.user.id)
            form.save()
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj, 'is_unique': form.instance.is_unique})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})


from django.views.generic import TemplateView


from .models import Post
from .forms import PostForm



class home(TemplateView):      
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect('home')
        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)
