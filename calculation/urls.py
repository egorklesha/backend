from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/indicators/search/', search_indicators),  # GET
    path('api/indicators/<int:indicator_id>/', get_indicator_by_id),  # GET
    path('api/indicators/<int:indicator_id>/image/', get_indicator_image),  # GET
    path('api/indicators/<int:indicator_id>/update/', update_indicator),  # PUT
    path('api/indicators/<int:indicator_id>/update_image/', update_indicator_image),  # PUT
    path('api/indicators/<int:indicator_id>/delete/', delete_indicator),  # DELETE
    path('api/indicators/create/', create_indicator),  # POST
    path('api/indicators/<int:indicator_id>/add_to_estimate/', add_indicator_to_estimate),  # POST

    # Набор методов для заявок
    path('api/estimates/', search_estimates),  # GET
    path('api/estimates/<int:estimate_id>/', get_estimate_by_id),  # GET
    path('api/estimates/<int:estimate_id>/update/', update_estimate),  # PUT
    path('api/estimates/<int:estimate_id>/update_status_user/', update_status_user),  # PUT
    path('api/estimates/<int:estimate_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/estimates/<int:estimate_id>/delete/', delete_estimate),  # DELETE
    path('api/estimates/<int:estimate_id>/delete_indicator/<int:indicator_id>/', delete_indicator_from_estimate),  # DELETE

    # Набор методов для м-м
    path('api/estimates/<int:estimate_id>/update_indicator/<int:indicator_id>/', update_estimate_indicator),  # PUT

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
