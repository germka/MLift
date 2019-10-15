from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    # Страница авторизации
    path('login/', views.login_base, name='login'),
    path('logout/', views.logout_base, name='logout'),
    # Список заявок
    path('', views.ticket_index, name='ticket_index'),
    # Окно заявки
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # Создание заявки
    path('newticket/', views.new_ticket, name='new_ticket'),
    # Закрытие заявки
    path('<int:ticket_id>/closed/', views.ticket_close, name='ticket_close'),
]