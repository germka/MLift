from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    # Список заявок
    path('', views.index, name='index'),
    # Окно заявки
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # Добавление комментария
    path('<int:ticket_id>/newcomment/', views.new_comment, name='new_comment'),
    # Создание заявки
    path('newticket/', views.new_ticket, name='new_ticket'),
]