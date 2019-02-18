from django.urls import path

from . import views

urlpatterns = [
    path('runloop/orders/<int:id>/result/', views.index, name='index'),
]