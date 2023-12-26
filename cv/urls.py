from django_distill import distill_path
# from django.urls import path

from . import views

urlpatterns = [
    distill_path("", views.index, name="index"),
]