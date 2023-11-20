from django.urls import path

from .views import *

urlpatterns = [
    # index отвечает за главную страницу сайта
    path('', index, name="home"),
    path('thematics/<int:indicator_id>', indicator_details, name="indicator_details"),
    # indicator_details - за информацию о показателе
    # Когда нажимаешь на кнопку "удалить" на карточке отправляется запрос на url thematic/id/delete
    # Вызывается вьюха indicator_delete
    path('thematics/<int:indicator_id>/delete/', indicator_delete, name="indicator_delete")
    # indicator_delete - за удаление показателя
]
