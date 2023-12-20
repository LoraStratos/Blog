from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('all_users/', AllUsers.as_view(), name='all_user'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', LoginViewMy.as_view(), name='login'),
    path('profile/<pk>', page_with_message, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/<pk>', update_page, name='update'),
    path('edit/<pk>', EditComment.as_view(), name='edit'),
    path('del_confirm/<pk>', DelComment.as_view(), name='del_confirm'),
    path('del_user/<pk>', wanna_delete, name='wanna_delete'),
    path('delete_user/<pk>', delete_u_and_p, name='delete1'),
]