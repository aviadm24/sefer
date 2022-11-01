# """avis URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('upload_image/', views.TaharaImageCreateView, name='TaharaImageCreateView'),
    path('list_image/', views.TaharaImageListView.as_view(), name='TaharaImageListView'),
    # path('list_image/', views.cloudinary_list, name='TaharaImageListView'),
    path('update_image/<slug:pk>/', views.TaharaImageUpdateView.as_view(), name='TaharaImageUpdateView'),
    path('incoming_sms/', views.incoming_sms, name='incoming_sms'),
    path('send_email/', views.send_email, name='send_email'),
    path('test_sms/', views.test_sms, name='test_sms'),
    path('incoming_answer_from_email/', views.incoming_answer_from_email, name='incoming_answer_from_email'),
    path('image_dashboard/', views.image_dashboard, name='image_dashboard'),
]
