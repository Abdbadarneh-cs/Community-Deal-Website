from django.urls import path
from .views import (
    deal_list, register_view, login_view, logout_view,
    verify_otp, add_deal_view, profile_view, profile_detail_view,
    toggle_like, deal_detail,user_profile_view
)

from .api_views import (
    DealListAPIView, DealDetailAPIView,
    FollowUserView, UnfollowUserView
)

urlpatterns = [
    #  Web views
    path('', deal_list, name='deal_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('add-deal/', add_deal_view, name='add_deal'),
    path('profile/', profile_detail_view, name='profile'),
    path('profile/edit/', profile_view, name='profile_edit'),
    path('deal/<int:deal_id>/', deal_detail, name='deal_detail'),
    path('deal/<int:deal_id>/like/', toggle_like, name='like_deal'),
    path('user/<int:user_id>/', profile_detail_view, name='profile_detail'),
    #  API views 
    path('api/deals/', DealListAPIView.as_view(), name='api_deal_list'),
    path('api/deals/<int:pk>/', DealDetailAPIView.as_view(), name='api_deal_detail'),
    path('api/follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('api/unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]