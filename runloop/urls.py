from django.urls import path

from . import views

urlpatterns = [
    path('runloop/runloopgroup/<int:id>/k/', views.index, name='index'),
]