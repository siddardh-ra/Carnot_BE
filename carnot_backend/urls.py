from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('carnot/users/', include("Users.urls")),
    path('carnot/project/', include("project_module.urls")),
    path('carnot/ftp/', include("ftp.urls")),
    path('carnot/draw/', include("drawtool.urls")),
]
