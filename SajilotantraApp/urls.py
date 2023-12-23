from django.urls import path

from . import views

urlpatterns = [
    path('', views.signup,name='index'),
    path('signup', views.signup,name='signup'),
    path('signin', views.signin,name='signin'),
    # path('admin', views.admin,name='admin'),
    path('events', views.events,name='events'),
    # path('play', views.playground,name='playground'),
    path('dashboard', views.dashboard,name='dashboard'),
    path("activate<uidb64>/<token>",views.activate,name="activate"),
    path('government_profiles',views.government_profiles,name='government_profiles'),
    path('government_profiles_details/<int:pk>/', views.government_profiles_details, name='government_profiles_details'),
    path('save_user_location',views.save_user_location,name='save_user_location'),
]