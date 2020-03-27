from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    # Страница авторизации
    path('logout/', views.logout_base, name='logout'),
    # Список заявок
    path('', views.ticket_index, name='ticket_index'),
    # фильтрованный список
    path('tickets/<str:index_filter>/', views.ticket_index, name='index_filter'),
    path('tickets/<str:index_filter>/<str:filter_str>/', views.ticket_index, name='index_filter'),
    # Окно заявки
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # Создание заявки
    path('newticket/', views.new_ticket, name='new_ticket'),
    # Закрытие заявки
    path('<int:ticket_id>/closed/', views.ticket_close, name='ticket_close'),
    # Изменение заявки
    path('<int:ticket_id>/changed/', views.ticket_edit, name='ticket_edit'),
    # Отчеты по заявкам
    path('summary/', views.ticket_summary, name="ticket_summary"),
    path('summary/<str:summary_filter>/', views.ticket_summary, name="ticket_summary"),
    path('summary/<str:summary_filter>/<str:summary_sort>', views.ticket_summary, name="ticket_summary"),
]