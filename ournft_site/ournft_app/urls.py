from django.urls import path
from django.conf.urls import include
from ournft_app import views

urlpatterns = [
    path('upload/', views.image_upload_view)
    
]