from django.urls import path
from django.conf.urls import include
from ournft_app import views

urlpatterns = [
    # path('', views.image_restore_view)
    path('restore/', views.image_restore_view),
    path('images/<slug:image_hash>/', views.image_view)
]