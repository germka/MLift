from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    # Список заявок
    path('', views.TicketIndexView.as_view(), name='index'),
    # Окно заявки
#    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'), 
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # Добавление комментария
#    path('<int:ticket_id>/', views.new_comment, name='new_comment'), comment add form moved to detail view
    # Создание заявки
    path('newticket/', views.new_ticket, name='new_ticket'),
]