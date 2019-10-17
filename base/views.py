from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
#from django.views import generic
from django.core.paginator import Paginator
#from django.template import loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import Ticket, TicketStatus, Object, ObjArea, ObjStr, ObjType, ManageComp

# Create your views here.

login_page = '/login/'

def logout_base(request):
    logout(request)
    return HttpResponseRedirect(login_page)


@login_required(login_url=login_page)
def ticket_index(request):
    if request.user.is_authenticated:
        paginator = Paginator(Ticket.objects.order_by('-ticket_date'), 20)
        page = request.GET.get('page')
        ticket_list = paginator.get_page(page)

        context = {
            'ticket_list': ticket_list,
        }
        return render(request, 'base/index.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))


@login_required(login_url=login_page)
def ticket_detail(request, ticket_id):
    if request.user.is_authenticated:
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
            ticket_object_exact = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build)
            if ticket.ticket_build_housing != None and ticket.ticket_build_housing != '':
                ticket_object_exact = ticket_object_exact.filter(obj_build_housing=ticket.ticket_build_housing)
            if ticket.ticket_par != None and ticket.ticket_par != '':
                ticket_object_exact = ticket_object_exact.filter(obj_par=ticket.ticket_par)
            if ticket.ticket_obj_type != None and ticket.ticket_obj_type != '':
                ticket_object_exact = ticket_object_exact.filter(obj_type=ticket.ticket_obj_type)
        except:
            context['error_message'] = "Объект с таким адресом не найден"
        else:
            try:
                ticket.ticket_object = ticket_object_exact.get()
            except (KeyError, Object.MultipleObjectsReturned):
                context['exact_message'] = "Выберите тип лифта:"
                obj_filter = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build)
                if ticket.ticket_build_housing:
                    obj_filter = obj_filter.filter(obj_build_housing=ticket.ticket_build_housing)
                if ticket.ticket_par:
                    obj_filter = obj_filter.filter(obj_par=ticket.ticket_par)
                if ticket.ticket_obj_type:
                    obj_filter = obj_filter.filter(obj_type=ticket.ticket_obj_type)
                context['object_exact'] = obj_filter
            except (KeyError, Object.DoesNotExist):
                context['error_message'] = "Адрес не верный, ни одного лифта не найдено"
            else:
                context['exact_message'] = "Лифт определен"
                context['exact_preview'] = ticket.ticket_object

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
    else:
        return HttpResponseRedirect(reverse('base:login'))


@login_required(login_url=login_page)
def new_ticket(request):
    if request.user.is_authenticated:
        ticket_number = Ticket.objects.last().id
        date_now = timezone.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")
        obj_str = ObjStr.objects.order_by('street')
        context = {
            'obj_str': obj_str,
            'ticket_number': ticket_number,
            'date_now': date_now,
        }
        if request.method == 'GET':
            context.update({
                'obj_build':'None',
                'obj_build_housing':'None',
                'obj_type':'None',
                'obj_par':'None',
            })
            return render(request, 'base/newticket.html', context)

        if request.method == 'POST':
            context['req'] = request.POST
            if 'ticket_content' in request.POST:
                new_content = request.POST['ticket_content']
                context['content_value'] = new_content

    #--obj filters

    #--obj_str handler

            if 'obj_str' in request.POST:
                if request.POST['obj_str'] == '':
                    context['help_message'] = "Выберите улицу"
                else:
                    try:
                        new_objstr = ObjStr.objects.get(street=request.POST['obj_str'])
                    except(KeyError, ObjStr.DoesNotExist):
                        context['error_message'] = "Значение улицы не заполнено"
                    except(KeyError, MultiValueDictKeyError):
                        context['error_message'] = "Улица не выбрана"
                    else:
                        context['str_value'] = new_objstr
                        filter_context = Object.objects.filter(obj_str=new_objstr)
                        context['obj_build'] = filter_context.values('obj_build').order_by('obj_build').distinct()	#--obj_build datalist

    #--obj_build handler

            if 'obj_build' in request.POST:
                if request.POST['obj_build'] == '':
                    context['help_message'] = "Выберите номер дома"
                else:
                    try:
                        new_objbuild = request.POST['obj_build']
                    except (KeyError, MultiValueDictKeyError):
                        context['error_message'] = "Дом не выбран"
                    else:
                        context['build_value'] = new_objbuild
                        filter_context = filter_context.filter(obj_build=new_objbuild)

    #--obj_build_housing check if exists

            obj_buildhousing = filter_context.values('obj_build_housing').order_by('obj_build_housing').distinct() #--obj_buildhousing filtered datalist

            if obj_buildhousing.count()>0:
                if obj_buildhousing[0]['obj_build_housing'] == None:
                    context['obj_buildhousing'] = None
                else:
                    context['obj_buildhousing'] = obj_buildhousing

    #--obj_build_housing handler

            if context['obj_buildhousing'] != None:
                if 'obj_buildhousing' in request.POST:
                    if request.POST['obj_buildhousing'] == '':
                        context['help_message'] = "Выберите корпус здания"
                    else:
                        try:
                            new_objbuildhousing = request.POST['obj_buildhousing']
                        except (KeyError, MultiValueDictKeyError):
                            context['error_message'] = "Корпус здания не выбран"
                        else:
                            context['build_housing_value'] = new_objbuildhousing
                            filter_context = filter_context.filter(obj_build_housing=new_objbuildhousing)
            else:
                new_objbuildhousing = None

    #--obj_par check if exists

            obj_par = filter_context.values('obj_par').order_by('obj_par').distinct() #--obj_par filtered datalist

            if obj_par.count()>0:
                if obj_par[0]['obj_par'] == None:
                    context['obj_par'] = None
                else:
                    context['obj_par'] = obj_par	#--obj_par datalist

    #--obj_par handler

            if 'obj_par' in request.POST:
                if request.POST['obj_par'] == '':
                    context['help_message'] = "Выберите парадную"
                else:
                    try:
                        new_objpar = request.POST['obj_par']
                    except (KeyError, MultiValueDictKeyError):
                        context['error_message'] = "Парадная не выбрана"
                    else:
                        if context['obj_par'] != None and new_objpar != 'None' and new_objpar != '':
                            filter_context = filter_context.filter(obj_par=new_objpar)
                        context['par_value'] = new_objpar

            obj_type = filter_context.values('obj_type').order_by('obj_type').distinct()	#obj_type filtered datalist
            if obj_type.count()>0:
                if obj_type[0]['obj_type'] == None:
                    context['obj_type'] = None
                else:
                    context['obj_type'] = ObjType.objects.filter(pk__in=obj_type)
    #        if filter_context.first().obj_type != None:
    #            context['obj_type'] = filter_context	#--obj_type datalist

    #--obj_type handler

            if 'obj_type' in request.POST:
                if request.POST['obj_type'] == '':
                    context['help_message'] = "Выберите тип лифта (из зарегистрированных)"
                else:
                    try:
                        new_objtype = ObjType.objects.get(type_name=request.POST['obj_type'])
                    except(KeyError, ObjType.DoesNotExist):
                        context['error_message'] = "Значение типа лифта не верно"

    #--ticket_date handler

            if 'ticket_date' in request.POST:
                new_date = request.POST['ticket_date']
            else:
                new_date = timezone.now().astimezone()	#--set current date

    #--making ticket

            if 'obj_str' in request.POST and 'obj_build' in request.POST and ('obj_par' in request.POST or 'obj_type' in request.POST):
                if request.POST['obj_str'] != '' and request.POST['obj_build'] != '':
                    if 'ticket_content' not in request.POST:	#--last check
                        context['error_message'] = "Содержание не может быть пустым"
                    else:
                        try:
                            ticket = Ticket(ticket_content=new_content, ticket_date=new_date, ticket_status_id=1, ticket_user=request.user, ticket_str=new_objstr, ticket_build=new_objbuild, )
                            if 'obj_buildhousing' in request.POST:
                                ticket.ticket_build_housing=new_objbuildhousing
                            if 'obj_par' in request.POST:
                                ticket.ticket_par=new_objpar
                            if 'obj_type' in request.POST:
                                if request.POST['obj_type'] != '':
                                    ticket.ticket_obj_type=new_objtype
                        except (KeyError, Object.DoesNotExist):
                            context['error_message'] = "Ошибка адреса либо типа лифта"
                        except (KeyError, Ticket.DoesNotExist):
                            context['error_message'] = "Заявка не создалась"
                        ticket.save()
                        return HttpResponseRedirect(reverse('base:ticket_index'))

    #--return

            return render(request, 'base/newticket.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))


@login_required(login_url=login_page)
def ticket_close(request, ticket_id):
    if request.user.is_authenticated:
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            context = {
                'ticket': ticket,
            }
        except (KeyError, Ticket.DoesNotExist):
            context['ticket_message'] = "Ошибка закрытия - заявка не существует"
        else:
            if 'obj_exact' in request.POST:
                ticket_obj = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build)
                if ticket.ticket_build_housing != None:
                    ticket_obj = ticket_obj.filter(obj_build_housing=ticket.ticket_build_housing)
                if ticket.ticket_par != None:
                    ticket_obj = ticket_obj.filter(obj_par=ticket.ticket_par)
                if request.POST['obj_exact'] != '':
                    ticket_obj = ticket_obj.filter(obj_type = ObjType.objects.get(type_name = request.POST['obj_exact']))
                else:
                    context['error_message'] = "Выберите лифт"

                try:
                    ticket.ticket_object = ticket_obj.get()
                except (KeyError, Object.MultipleObjectsReturned):
                    context['error_message'] = "Сразу несколько лифтов выбрано из базы, требуется корректировка списка лифтов"
                else:
                    ticket.save()	#--save ticket after chiose
            elif 'ticket_obj' in request.POST:
                ticket.ticket_object = Object.objects.get(pk=request.POST['ticket_obj'])
                ticket.save() #--save ticket without choise

            context['ticket_object'] = ticket.ticket_object

            if ticket.ticket_object != None:
                ticket.close()	#--close ticket
                ticket.duration_save()
                context['ticket_message'] = "Заявка успешно закрыта"

        return render(request, 'base/detail.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))
