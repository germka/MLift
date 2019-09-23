from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
#from django.template import loader

from .models import Ticket, TicketStatus, Object, ObjStr, ObjType, ManageComp

# Create your views here.

class TicketIndexView(generic.ListView):
    template_name = 'base/index.html'
    context_object_name = 'latest_ticket_list'

    def get_queryset(self):
        return Ticket.objects.order_by('-ticket_date')[:20]


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    context = {
        'ticket': ticket,
    }
    try:
        content = request.POST['comment_content']
    except (KeyError, Ticket.DoesNotExist):
        return render(request, 'base/detail.html', { 'ticket': ticket, })
    else:
        if content != "":
            if content != ticket.comments_set.last().comment_content:
                ticket.comments_set.create(comment_content=content, comment_date=timezone.now())
                return render(request, 'base/detail.html', { 'ticket': ticket, 'message':"Комментарий успешно добавлен", })
            else:
                return render(request, 'base/detail.html', { 'ticket': ticket, })
        else:
            return render(request, 'base/detail.html', { 'ticket': ticket, 'errormessage':"Комментарий не должен быть пустым", })


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


#def new_comment(request, ticket_id):
#    try:
#        content = request.POST['comment_content']
#        ticket = Ticket.objects.get(pk=ticket_id)
#    except (KeyError, Ticket.DoesNotExist):
#        return render(request, 'base/detail.html', { 'errormessage':"Комментарий не должен быть пустым", })
#    else:
#        if content != "":
#            ticket.comment_set.create(comment_content=content, comment_date=timezone.now())
#            return render(request, 'base/detail.html', { 'message':"Комментарий успешно добавлен", })