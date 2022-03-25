from django.urls import path
# #<<<<<<< likes
# from . import views

# urlpatterns = [
#     path('', views.PostIndexView.as_view(), name='post-list'),
#     path('tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),
#     path('detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
#     
# ]
# #=======
from django.conf.urls import include
from ournft_app import views

urlpatterns = [

    path('restore/', views.image_restore_view),
  
    path('images/<slug:image_hash>/', views.image_view, name='image_detail'),

    path('like/<slug:image_hash>', views.ImageLike, name='image_like'),
]
#>>>>>>> main
