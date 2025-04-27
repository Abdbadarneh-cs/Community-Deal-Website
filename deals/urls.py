from django.urls import path
from .views import deal_list, register_view, login_view, logout_view, verify_otp , add_deal_view

urlpatterns = [
    path('', deal_list, name='deal_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('add-deal/', add_deal_view, name='add_deal'),
]
