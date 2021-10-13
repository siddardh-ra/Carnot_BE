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
    path('create_project/', views.create, name="create"),
    path('add_date/<slug:p_name>/<slug:date>', views.add_date, name="date"),
    path('environmental/<slug:p_name>/<slug:date>', views.save_environment_details, name="environmental"),
    path('payload/<slug:p_name>/<slug:date>', views.save_payload_details, name="payload"),
    path('get_project/<slug:name>', views.get_project, name="payload"),
    path('get_all/',views.ProjectListApiView.as_view(),name="project_data"),
    path('get_recent_projects/',views.Recent_project_List,name="project_data"),
    url('^summary_data_dump/(?P<project_name>[\w\ -]+)$', views.dump_summary_data, name="dump_summary_data"),
    url('^inverter_data_dump/(?P<project_name>[\w\ -]+)$', views.dump_inverter_data, name="dump_inverter_data"),
    url('^retrieve_summary_data/(?P<project_name>[\w\ -]+)$', views.retrieve_summary_data, name="retrieve_summary_data"),
    url('^retrieve_inverter_data/(?P<project_name>[\w\ -]+)$', views.retrieve_inverter_data, name="retrieve_inverter_data"),
    url('^data/(?P<project>[\w\ -]+)/(?P<date>[\w\ -]+)$',views.get_project_data_by_date,name="update"),
    url('^retrieve_project_data/(?P<project>[\w\ -]+)$',views.retrieve_project_data,name="update"),
    path('get_projects_status/', views.get_projects_status, name="get_projects_status"),
    url('^add_new_date/(?P<p_name>[\w\ -]+)/(?P<date>[\w\ -]+)$', views.add_new_date, name="date"),
    path('get_dashboard_data/', views.get_dashboard_data, name="get_dashboard_data"),
]
