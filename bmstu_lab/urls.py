from django.urls import path
from .views import *

urlpatterns = [
    path('', RentsListPage, name='rents'),
    path('rents/<int:id>/', RentDetailsPage, name='rent_details'),
]
