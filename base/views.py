from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
#from django.views import generic
from django.core.paginator import Paginator
#from django.template import loader

from .models import Ticket, TicketStatus, Object, ObjArea, ObjStr, ObjType, ManageComp

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
        'obj_type': ObjType.objects.all(),
    }

    try:
        ticket_object = Object.objects.get(pk=ticket.ticket_object.id)
    except:
        context['no_object_message'] = "Лифт пока не определен"
    else:
        context['ticket_object'] = ticket_object

    try:
        ticket_object_exact = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build, obj_biuld_housing=ticket.ticket_build_housing, obj_par=ticket.ticket_par)
    except:
        context['error_message'] = "Объект с таким адресом не найден"
    else:
        try:
            ticket.ticket_object = ticket_object_exact.get()
        except (KeyError, Object.DoesNotExist):
            content['exact_message'] = "Выберите тип лифта"
            context['object_exact'] = ticket_object_exact.obj_type.values('obj_type').order_by('obj_type').distinct()
        else:
            context['exact_message'] = "Лифт определен"

    if request.method == 'GET':
        return render(request, 'base/detail.html', context)
    if request.method == 'POST':
        try:
            content = request.POST['comment_content']
        except:
            content = ''
        user = request.user.first_name + ' ' + request.user.last_name
        try:
            last_content = ticket.comments_set.last().comment_content
        except:
            last_content = ''
        if content != "":
            if content != last_content:
                ticket.comments_set.create(comment_content=content, comment_date=timezone.now(), comment_user = user)
                context['message'] = "Комментарий успешно добавлен"
        else:
            context['errormessage'] = "Комментарий не должен быть пустым"
        return render(request, 'base/detail.html', context)




def new_ticket(request):
    manage_comp = ManageComp.objects.order_by('comp_name')
    obj_area = ObjArea.objects.order_by('area_name')
    obj_str = ObjStr.objects.order_by('street')
    obj_build = Object.objects.values('obj_build').order_by('obj_build').distinct()
    obj_buildhousing = Object.objects.values('obj_build_housing').order_by('obj_build_housing').distinct()
    obj_type = ObjType.objects.order_by('type_name')
    objects_query = Object.objects.all()
    ticket_number = Ticket.objects.count()
    context = {
        'manage_comp': manage_comp,
        'obj_area': obj_area,
        'obj_str': obj_str,
        'obj_build': obj_build,
        'obj_buildhousing':obj_buildhousing,
        'obj_type': obj_type,
        'objects_query': objects_query,
        'ticket_number': ticket_number,
    }
    if request.method == 'GET':
        return render(request, 'base/newticket.html', context)

    if request.method == 'POST':
        status = TicketStatus.objects.get(pk=1)
        new_content = request.POST['ticket_content']

#--obj filters

        try:
            new_objstr = ObjStr.objects.get(street=request.POST['obj_str'])
        except(KeyError, ObjStr.DoesNotExist):
            context['error_message'] = "Значение улицы не заполнено"


        new_objbuild = request.POST['obj_build']
        if new_objbuild == '':
            context['error_message'] = "Значение номера дома не заполнено"


        try:
            new_objbuildhousing = request.POST['obj_build_housing']
        except:
            new_objbuildhousing = ''


        new_objpar = request.POST['obj_par']
        if new_objpar == '':
            context['error_message'] = "Значение номера парадной не введено"


        try:
            new_objtype = ObjType.objects.get(type_name=request.POST['obj_type'])
        except(KeyError, ObjType.DoesNotExist):
            context['error_message'] = "Значение типа лифта не верно"


        new_date = request.POST['ticket_date']
        if new_date == "":
            new_date = timezone.now()

#--make ticket

        try:
            ticket = Ticket(ticket_content=new_content, ticket_date=new_date, ticket_status=status, ticket_user=1, ticket_str=new_objstr, ticket_build=new_objbuild, ticket_build_housing=new_objbuildhousing, ticket_par=new_objpar)
        except (KeyError, Object.DoesNotExist):
            context['error_message'] = "Ошибка в параметрах"

#--last check

        if new_content == "":
            context['error_message'] = "Содержание не может быть пустым"
            return render(request, 'base/newticket.html', context)
        else:
            ticket.save()
            return HttpResponseRedirect(reverse('base:ticket_index'))



def ticket_close(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_object = Object.objects.get(pk=ticket.ticket_object.id)
        context = {
            'ticket': ticket,
            'ticket_object': ticket_object,
        }

    except (KeyError, TicketDoesNotExist):
        context['ticket_message'] = "Ошибка закрытия - заявка не существует"
    else:
        ticket.close()
        context['ticket_message'] = "Заявка успешно закрыта"
    return render(request, 'base/detail.html', context)
