"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cs412/quotes/', include('quotes.urls')),
    path('cs412/restaurant/', include('restaurant.urls')),
    path('cs412/mini_insta/', include('mini_insta.urls')),
    path('cs412/voter_analytics/', include('voter_analytics.urls')),
    path('cs412/dadjokes/', include('dadjokes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # BU webapps strips "/alvinz" before routing to Django.
    # Provide compatibility routes for local path seen by Django.
    urlpatterns += static('/cs412/static/', document_root=settings.STATIC_ROOT)
    urlpatterns += static('/cs412/media/', document_root=settings.MEDIA_ROOT)
