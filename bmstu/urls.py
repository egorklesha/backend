from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Список
    path('', views.Get_rent_calculation_s, name='rent_calculation_s'),

    # Информация
    path('rent_calculation/<int:id>/', views.Get_rent_calculation, name='about_rent_calculation'),

    # Фильтрация
    path('rent_calculation/', views.Filter, name='filter'),

]
