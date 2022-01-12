"""djangoTP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from sim_manager import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.landing),
    path('account/', include('django.contrib.auth.urls')),
    url(r'^profile/', views.edit_profile,name="profile"),
    url(r'^sim_list/', views.simulation_list,name="sim_list"),
    url(r'^$', views.landing),
    url(r'^newsimu/$', views.new_simu, name='newsimu'),
    url(r'^(?P<object_id>[0-9]+)/run_sim/$', views.run_sim, name='run_sim'),
    url(r'^(?P<object_id>[0-9]+)/delete_sim/$', views.simulation_delete, name='delete_sim'),
    url('user/new', views.creer_utilisateur, name='creer_utilisateur'),
    url('user/info', views.user_info, name='user_info'),
    url('user/logout', views.logout_view, name='logout'),
    url('user/login', views.login_view, name='login')
]
