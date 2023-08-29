"""
URL configuration for OpenWMS project.

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
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from tools import tinymce_upload
from utils.vaptcha.vaptcha import CustomLoginView

admin.autodiscover()

urlpatterns = [
    path(r"tinymce/ ", include("tinymce.urls")),
    path(r'tinymce/upload_image/', tinymce_upload.upload_image),
    path(r"admin/", admin.site.urls),
    path(r"api/v1/", include("api.urls")),
    path(r"exim/", include("im_export.urls")),
]

if settings.VAPTCHA_IN_ADMIN:
    urlpatterns = [
        path(r'admin/login/', CustomLoginView.as_view(), name='login'),
    ] + urlpatterns

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
