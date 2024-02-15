from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('indicators/<int:indicator_id>/', indicator_details),
    path('indicators/<int:indicator_id>/delete/', indicator_delete),
    path('estimates/<int:estimate_id>/', estimate_details)
]
