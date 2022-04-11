from django.urls import path
from django.conf.urls import include
from ournft_app import views

appname = 'ournft_app'

urlpatterns = [

    path('restore/', views.image_restore_view),
  
    path('images/<slug:image_hash>/', views.image_view, name='image_detail'),

    path('like/<slug:image_hash>', views.ImageLike, name='image_like'),

    path('transfer/', views.image_transfer_view),

    path('notification/<slug:id>', views.GetTransfer, name='notification'),

    path('create_comment/<slug:image_hash>', views.CommentView.as_view(), name='comment'),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('feed/', views.FeedView.as_view(), name='feed')
]
