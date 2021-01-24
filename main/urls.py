"""sefaria_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('index/<int:number>/', views.index, name="index"),
    path('titles/', views.titles, name="titles"),
    re_path(r'^api/texts/(?P<slug>[a-zA-Z,_ ]*)/$', views.texts),
    path('api/texts/<slug:slug>/', views.texts),
    re_path(r'^api/texts/(?P<slug>[a-zA-Z,_ ]*)/(?P<chapter>[0-9]*)$', views.texts),
    path('api/texts/<slug:slug>/<int:chapter>', views.texts),
]
