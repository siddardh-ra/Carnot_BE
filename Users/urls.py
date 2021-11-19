"""agri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',views.home,name="login"),
    path('create/',views.create,name="create"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="reset_password/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset_password/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password/password_reset_done.html"), name="password_reset_complete"),
    # path('listall/',views.ListAllUser.as_view(),name="listAll"),
    # url('^list/(?P<user>[\w-]+)$', views.get_user, name="list"),
    # url("^password_reset/(?P<user>[\w-]+)$",views.password_reset,name="password_reset"),
    # url('^password_reset/(?P<user>[\w-]+)/(?P<token>[a-zA-Z0-9_-]*)$',views.check_token,name="password_reset_check"),
    # url('^change_password/(?P<user>[\w-]+)',views.change_password,name="change_password")
 ]
