from django.shortcuts import render, redirect

# Create your views here.

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
