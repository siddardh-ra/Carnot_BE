from django.urls import path, re_path
from . import views

urlpatterns = [
    path('create_project/', views.create, name="create"),
    path('add_date/<slug:p_name>/<slug:date>', views.add_date, name="date"),
    path('environmental/<slug:p_name>/<slug:date>', views.save_environment_details, name="environmental"),
    path('payload/<slug:p_name>/<slug:date>', views.save_payload_details, name="payload"),
    path('get_project/<slug:name>', views.get_project, name="payload"),
    path('get_all/',views.ProjectListApiView.as_view(),name="project_data"),
    path('get_recent_projects/',views.Recent_project_List,name="project_data"),
    re_path('^summary_data_dump/(?P<project_name>[\w\ -]+)$', views.dump_summary_data, name="dump_summary_data"),
    re_path('^inverter_data_dump/(?P<project_name>[\w\ -]+)$', views.dump_inverter_data, name="dump_inverter_data"),
    re_path('^retrieve_summary_data/(?P<project_name>[\w\ -]+)$', views.retrieve_summary_data, name="retrieve_summary_data"),
    re_path('^retrieve_inverter_data/(?P<project_name>[\w\ -]+)$', views.retrieve_inverter_data, name="retrieve_inverter_data"),
    re_path('^data/(?P<project>[\w\ -]+)/(?P<date>[\w\ -]+)$',views.get_project_data_by_date,name="update"),
    re_path('^retrieve_project_data/(?P<project>[\w\ -]+)$',views.retrieve_project_data,name="update"),
    path('get_projects_status/', views.get_projects_status, name="get_projects_status"),
    re_path('^add_new_date/(?P<p_name>[\w\ -]+)/(?P<date>[\w\ -]+)$', views.add_new_date, name="date"),
    path('get_dashboard_data/', views.get_dashboard_data, name="get_dashboard_data"),
    re_path('^share_project/(?P<id>[\w\ -]+)$', views.share_project, name="share_project"),
    path('update', views.update)
]
