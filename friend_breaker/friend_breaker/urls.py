"""friend_breaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from fb_app.views import index, about, profile, update, authorization, logout


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index, name="index"),
    url(r'^about/', about, name="about"),
    url(r'^profile/', profile, name="profile"),

    url(r'^update/', update, name="update"),

    url(r'^authorization/', authorization, name="authorization"),
    url(r'^logout/', logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
