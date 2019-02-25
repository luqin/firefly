from django.urls import path

from . import views

urlpatterns = [
    path('runloop/runloopgroup/<int:id>/k/', views.k, name='k'),
    path('runloop/runloopgroup/<int:id>/returns/', views.returns, name='k'),
]