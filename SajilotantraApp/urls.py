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
    
    path("activate<uidb64>/<token>",views.activate,name="activate")
]