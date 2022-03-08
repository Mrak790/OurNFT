from django.shortcuts import render

# Create your views here.
from .forms import ImageForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin')
def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            is_unique = form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj, 'is_unique': is_unique})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})