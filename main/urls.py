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
    path('', views.home, name="home"),
    path('index/<int:number>/', views.index, name="index"),
    path('titles/', views.titles, name="titles"),
    re_path(r"^api/texts/(?P<slug>[a-zA-Z0-9,'_:. +-]*)/$", views.texts),
    # re_path(r"^api/commentators/(?P<slug>[a-zA-Z0-9,'_:. +-]*)/$", views.texts_with_commentators),
    path('get_comment/', views.get_comment, name='validate_username'),
    path('profile/', views.YcommentListView.as_view(), name='ycomment-list'),
    path('add_comment/', views.add_comment, name="add_comment"),
    path('remove_comment/<int:id>/', views.remove_comment, name="remove_comment"),
    path('is_authenticated/', views.is_authenticated),
    path('add_file/', views.add_file),
    path('contact/', views.contact),
    path('about/', views.about),
    path('dashboard/', views.dashboard),
    path('search_results/', views.search_results),
    path('search_titles/', views.search_titles),
    path('mechkar/', views.excel_parsing, name='excel_parsing'),
]