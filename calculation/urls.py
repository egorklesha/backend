from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('thematics/<int:indicator_id>', indicator_details, name="indicator_details"),
    path('thematics/<int:indicator_id>/delete/', indicator_delete, name="indicator_delete")
]
