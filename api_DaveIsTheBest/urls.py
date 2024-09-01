"""
URL configuration for api_DaveIsTheBest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve

admin.site.site_header = 'Dave Is The Best Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("comments/", include("comments.urls")),
    path("interval-timer/", include("interval_timer.urls")),
    path("davestech_contacts/", include("davestech_contacts.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("base_app.urls")),
]

if not settings.PRODUCTION:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns.append(
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    )