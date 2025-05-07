from django.urls import path
from .views import deal_list, register_view, login_view, logout_view, verify_otp , add_deal_view ,profile_view, profile_detail_view, toggle_like
# from . import views
urlpatterns = [
    path('', deal_list, name='deal_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('add-deal/', add_deal_view, name='add_deal'),
    path('profile/', profile_detail_view, name='profile'),
    path('profile/edit/', profile_view, name='profile_edit'),
    path('deal/<int:deal_id>/like/', toggle_like, name='toggle_like'),
    path('deal/<int:deal_id>/like/', toggle_like, name='like_deal'),
    

]
