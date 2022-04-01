from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/',login_required(views.logout_view,login_url='home'), name='logout'),
    path('profile/', login_required(views.profile_view.as_view(), login_url='home'), name='profile'),
    path('profile/edit/', login_required(views.EditProfileView.as_view(),login_url='home'), name='edit_profile'),
    path('set_avatar/<slug:image_hash>', views.SetAvatar, name='set_avatar')
  
]