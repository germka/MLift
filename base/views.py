from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
#from django.template import loader

from .models import Ticket

# Create your views here.

def index(request):
    latest_ticket_list = Ticket.objects.order_by('-ticket_date')[:20]
    context = {
        'latest_ticket_list': latest_ticket_list,
    }
    return render(request, 'base/index.html', context)

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    context = {
        'ticket': ticket,
    }
    return render(request, 'base/detail.html', context)

def new_ticket(request):
    return HttpResponse("Создать заявку")

def new_comment(request, ticket_id):
    return HttpResponse("Добавить комментарий к заявке №%s" % ticket_id)