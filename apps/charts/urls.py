from django.urls import path

from . import views
from .views_k import k

urlpatterns = [
    path('', views.index, name='index'),
    path('k/', k.index, name='k'),
    path('k1/', views.k, name='k1'),
]