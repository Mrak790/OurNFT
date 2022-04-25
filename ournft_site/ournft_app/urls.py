from django.urls import path
from django.conf.urls import include
from ournft_app import views

appname = 'ournft_app'

urlpatterns = [

    path('restore/', views.ImageRestoreView.as_view()),
  
    path('images/<slug:image_hash>/', views.ImageView.as_view()),

    path('like/<slug:image_hash>/', views.ImageLikeView.as_view(), name='image_like'),

    path('transfer/', views.ImageTransferView.as_view(), name='transfer'),

    path('notification/<slug:id>/', views.GetTransferView.as_view(), name='notification'),

    path('create_comment/<slug:image_hash>/' , views.CommentView.as_view(), name='comment'),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('feed/', views.FeedView.as_view(), name='feed'),
    
    path('report/', views.ReportView.as_view(), name='report'),

    path('report_list/', views.ReportListView.as_view(), name='report_list'),

    path('delete_comment/<slug:id>', views.DeleteCommentView.as_view(), name='delete_comment'),

    path('ban_image/<slug:image_hash>', views.BanImageView.as_view(), name='ban_image'),

    path('ban_user/', views.BanUserView.as_view(), name='ban_user'),

    path('switch_visibility/<slug:image_hash>', views.SwitchVisibleView.as_view(), name='switch_visibility'),

    path('token_restore/', views.TokenRestoreView.as_view(), name='token_restore'),
]
