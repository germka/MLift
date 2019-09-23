from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
#from django.views import generic
from django.core.paginator import Paginator
#from django.template import loader

from .models import Ticket, TicketStatus, Object, ObjStr, ObjType, ManageComp

# Create your views here.

def ticket_index(request):
    paginator = Paginator(Ticket.objects.order_by('-ticket_date'), 20)

    page = request.GET.get('page')
    ticket_list = paginator.get_page(page)
    context = {
        'ticket_list': ticket_list,
    }
    return render(request, 'base/index.html', context)


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    context = {
        'ticket': ticket,
    }
    if request.method == 'GET':
        return render(request, 'base/detail.html', context)
    if request.method == 'POST':
        content = request.POST['comment_content']
        try:
            last_content = ticket.comments_set.last().comment_content
        except:
            last_content = null
        if content != "":
            if content != last_content:
                ticket.comments_set.create(comment_content=content, comment_date=timezone.now())
                context['message'] = "Комментарий успешно добавлен"
        else:
            context['errormessage'] = "Комментарий не должен быть пустым"
        return render(request, 'base/detail.html', context)


def new_ticket(request):
    manage_comp = ManageComp.objects.order_by('comp_name')
    obj_str = ObjStr.objects.order_by('street')
    obj_type = ObjType.objects.order_by('type_name')
    objects_query = Object.objects.all()
    ticket_number = Ticket.objects.count()
    context = {
        'manage_comp': manage_comp,
        'obj_str': obj_str,
        'obj_type': obj_type,
        'objects_query': objects_query,
        'ticket_number': ticket_number,
    }
    status = TicketStatus.objects.get(pk=1)
    try:
        content = request.POST['ticket_content']
        ticket = Ticket(ticket_content=content, ticket_date=timezone.now(), ticket_status=status, ticket_user=1)
    except (KeyError, Ticket.DoesNotExist):
        return render(request, 'base/newticket.html', context)
    else:
        if content == "":
            return render(request, 'base/newticket.html', {
                'error_message': "Содержание не может быть пустым",
            })
        else:
            ticket.save()
            return HttpResponseRedirect(reverse('base:index'))

