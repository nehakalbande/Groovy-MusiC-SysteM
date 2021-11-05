from django.urls import path
from . import views

# Add URLConf
urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('signup/', views.signup_request, name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('userinfo/',views.getUserDetails,name='dummy-user'),
    path('friends/',views.friend_list,name='friend_list'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('search_users/',views.search_users,name='search_users'),
    path('users_list/',views.users_list,name='users_list'),
    path('<slug>/', views.profile_view, name='profile_view'),
    path('friend-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
	path('friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
	path('friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
	path('friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
	path('friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
]
