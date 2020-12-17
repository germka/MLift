from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
#from django.views import generic

#!--index
from django.core.paginator import Paginator
#from django.template import loader

#!--summary
import csv
from django.db.models import Q

#!--common
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import timezone
from datetime import datetime

from .models import Ticket, TicketType, TicketStatus, Object, ObjArea, ObjStr, ObjType, ManageComp, FUR_group, FUReason, Worker

# Create your views here.

login_page = '/login/'
paginator_list_size = 50

def logout_base(request):
    logout(request)
    return HttpResponseRedirect(login_page)


@login_required(login_url=login_page)
def ticket_index(request, index_filter=None, filter_str=None):
    if request.user.is_authenticated:
        context = {
            'str_filter': ObjStr.objects.all(),
        }
        if not index_filter:
            ticket_query = Ticket.objects.order_by('-ticket_date')
            context['no_filter'] = True
        elif index_filter == "area":
            ticket_query = Ticket.objects.order_by('-ticket_date__year', '-ticket_date__month', '-ticket_date__day', 'ticket_str__area', '-id')
            context['splitter'] = "area"
        elif index_filter == "str":
            if filter_str:
                ticket_query = Ticket.objects.filter(ticket_str__street__contains=filter_str).order_by('-ticket_date__year', '-ticket_date__month', '-ticket_date__day', 'ticket_str', '-id')
                context['splitter'] = "str"
            else:
                ticket_query = Ticket.objects.order_by('-ticket_date__year', '-ticket_date__month', '-ticket_date__day', 'ticket_str', '-id')
                context['splitter'] = "str"
        elif index_filter == "status":
            ticket_query = Ticket.objects.order_by('-ticket_date__year', '-ticket_date__month', '-ticket_date__day', 'ticket_status', '-id')
            context['splitter'] = "status"
        elif index_filter == "owner":
            ticket_query = Ticket.objects.order_by('-ticket_date__year', '-ticket_date__month', '-ticket_date__day', 'ticket_object__manage_comp', '-id')
            context['splitter'] = "owner"
        elif {'street':index_filter} in ObjStr.objects.all().values('street'):
            ticket_query = Ticket.objects.filter(ticket_str__street__contains=index_filter).order_by('-ticket_date')
        elif {'status':index_filter} in TicketStatus.objects.all().values('status'):
            ticket_query = Ticket.objects.filter(ticket_status__status__contains=index_filter).order_by('-ticket_date')

        paginator = Paginator(ticket_query, paginator_list_size)
        page = request.GET.get('page')
        ticket_list = paginator.get_page(page)

        context['ticket_list']= ticket_list

        return render(request, 'base/index.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))


@login_required(login_url=login_page)
def ticket_detail(request, ticket_id):
    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        date_now = timezone.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")
        context = {
            'ticket': ticket,
            'obj_type': ObjType.objects.all(),
            'workers': Worker.objects.filter(active=True).filter(worker_area = ticket.ticket_str.area),
            'FUR': FUR_group.objects.all(),
            'date_now': date_now,
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
            elif ticket.ticket_build_housing == None:
                ticket_object_exact = ticket_object_exact.filter(obj_build_housing=None) 
            if ticket.ticket_par != None and ticket.ticket_par != '':
                ticket_object_exact = ticket_object_exact.filter(obj_par=ticket.ticket_par)
            context['objects_list'] = ticket_object_exact
        except:
            context['error_message'] = "Объект с таким адресом не найден"
        else:
            try:
                ticket.ticket_object = ticket_object_exact.get()
                context['exact_message'] = "Лифт определен"
                context['exact_preview'] = ticket.ticket_object

            except (KeyError, Object.MultipleObjectsReturned):
                context['exact_message'] = "Выберите тип лифта:"
                obj_filter = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build, obj_in_service = True)
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
#                context['exact_message'] = "Лифт определен"
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

        if Ticket.objects.last():
            ticket_number = Ticket.objects.last().id
        else:
            ticket_number = 0
        date_now = timezone.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")
        obj_str = [str['obj_str__street'] for str in Object.objects.filter(obj_in_service = True).values('obj_str__street').distinct().order_by('obj_str__street')]
        context = {
            'obj_str': obj_str,
            'ticket_number': ticket_number,
            'date_now': date_now,
            'FUR': FUR_group.objects.all(),
            'ticket_type': TicketType.objects.all(),
        }
        if request.method == 'GET':
            context.update({
                'obj_build':'None',
                'obj_buildhousing':'None',
                'obj_type':'None',
                'obj_par':'None',
            })
            return render(request, 'base/newticket.html', context)

        if request.method == 'POST':
#            context['req'] = request.POST
            new_objbuildhousing = None
            new_objpar = None
            new_objtype = None
            if 'ticket_content' in request.POST:
                new_content = request.POST['ticket_content']
                context['content_value'] = new_content
            elif 'ticket_content_placeholder' in request.POST:
                context['content_value'] = request.POST['ticket_content_placeholder']
            if 'ticket_sender' in request.POST:
                context['sender_value'] = request.POST['ticket_sender']
            if 'ticket_type' in request.POST:
                context['type_value'] = request.POST['ticket_type']

    #--obj filters
            filter_context = Object.objects.filter(obj_in_service=True)
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
                        filter_context = filter_context.filter(obj_str=new_objstr)
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
                    elif request.POST['obj_buildhousing'] == 'Нет':
                        filter_context = filter_context.filter(obj_build_housing = None)
                        context['build_housing_value'] = request.POST['obj_buildhousing']
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
            context['test'] = filter_context

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
                    context['help_message'] = "Выберите тип лифта"
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

    #--make new ticket

            if 'obj_str' in request.POST:
                if request.POST['obj_str'] != '':
                    context['help_message'] = 'Выберите дом'
                else:
                    context['help_message'] = 'Выберите улицу'

            if 'sender' in request.POST:
                if request.POST['sender'] == 'jQuery':
                    return render(request, 'base/newticket.html', context)

            if 'obj_str' in request.POST and 'obj_build' in request.POST:
                if request.POST['obj_str'] != '' and request.POST['obj_build'] != '':
                    context['help_message'] = 'Выбор из списка'

                    if (filter_context.first().obj_build_housing != None or filter_context.values('obj_build_housing').order_by('obj_build_housing').distinct().count() > 1) and not new_objbuildhousing:
                        context['help_message'] = 'Выберите корпус'
                    elif (filter_context.first().obj_par != None or filter_context.values('obj_par').order_by('obj_par').distinct().count() > 1) and not new_objpar:
                        context['help_message'] = 'Выберите парадную'
                    elif 'ticket_type' not in request.POST or request.POST['ticket_type'] == '':	#--last check
                        context['help_message'] = "Введите тип заявки"


                    else:
                        context['help_message'] = "Готов создать заявку"

                        try:
                            ticket = Ticket(ticket_content=new_content, ticket_date=new_date, ticket_status_id=1, ticket_user=request.user, ticket_str=new_objstr, ticket_build=new_objbuild, )
                        except (KeyError, Object.DoesNotExist):
                            context['error_message'] = "Ошибка адреса либо типа лифта"
                        except (KeyError, Ticket.DoesNotExist):
                            context['error_message'] = "Заявка не создалась"
                        else:
                            if 'obj_buildhousing' in request.POST:
                                ticket.ticket_build_housing=new_objbuildhousing
                            if 'obj_par' in request.POST:
                                ticket.ticket_par=new_objpar
                            if 'obj_type' in request.POST:
                                if request.POST['obj_type'] != '':
                                    ticket.ticket_obj_type=new_objtype
                            if 'ticket_type' in request.POST:
                                ticket.ticket_type=TicketType.objects.get(type_name = request.POST['ticket_type'])
                            if 'ticket_sender' in request.POST:
                                ticket.ticket_sender=request.POST['ticket_sender']
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
                else:
                    ticket_obj = ticket_obj.filter(obj_build_housing=None)
                if ticket.ticket_par != None:
                    ticket_obj = ticket_obj.filter(obj_par=ticket.ticket_par)
                if request.POST['obj_exact'] != '':
                    ticket_obj = ticket_obj.filter(obj_type = ObjType.objects.get(type_name = request.POST['obj_exact']))
                else:
                    context['error_message'] = "Выберите лифт"

                try:
                    ticket.ticket_object = ticket_obj.get()
                except (KeyError, Object.MultipleObjectsReturned):
                    context['error_message'] = "Несколько лифтов выбрано из базы, требуется корректировка списка лифтов"
                else:
                    ticket.save()	#--save ticket after chiose
            elif 'ticket_obj' in request.POST:
                ticket.ticket_object = Object.objects.get(pk=request.POST['ticket_obj'])
                ticket.save() #--save ticket without choise

            context['ticket_object'] = ticket.ticket_object

            if 'worker_exact' in request.POST:
                full_name = request.POST['worker_exact'].split(' ',1)
                worker = Worker.objects.filter(first_name__contains=full_name[1], last_name__contains=full_name[0])
                ticket.ticket_worker = worker.get()

            if 'ticket_content' in request.POST:
                ticket.ticket_content = request.POST['ticket_content']

            if ticket.ticket_object != None:
                ticket.close()	#--close ticket
                ticket.duration_save()
                context['ticket_message'] = "Заявка успешно закрыта"

        return HttpResponseRedirect(reverse('base:ticket_detail', args=[ticket_id]))
#        return render(request, 'base/detail.html', context)
    else:
        return HttpResponseRedirect(reverse('base:login'))


@login_required(login_url=login_page)
def ticket_edit(request, ticket_id):
    if request.user.is_staff:
        context = {
        }
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except (KeyError, Ticket.DoesNotExist):
            context['ticket_message'] = "Ошибка сохранения - заявка не существует"
        else:
            if 'change_object' in request.POST and request.POST['change_object'] != '':
                ticket_object = Object.objects.filter(obj_str=ticket.ticket_str, obj_build=ticket.ticket_build, obj_build_housing=ticket.ticket_build_housing, obj_par=ticket.ticket_par, obj_type__type_name__contains=request.POST['change_object'])
                try:
                    new_object = ticket_object.get()
                except (KeyError, Object.MultipleObjectsReturned):
                    context['error_message'] = "Несколько лифтов выбрано из базы, требуется корректировка списка лифтов"
                else:
                    ticket.ticket_object = new_object
            if 'reopen_ticket' in request.POST:
                if request.POST['reopen_ticket'] == 'on':
                    ticket.ticket_status_id = 1
                    ticket.ticket_duration = None
            if 'new_ticket_date' in request.POST:
                if request.POST['new_ticket_date'] != '':
                    new_date = request.POST['new_ticket_date']
                    ticket.ticket_duration = datetime.strptime(new_date, '%Y-%m-%dT%H:%M:%S').astimezone() - ticket.ticket_date
            if 'new_worker' in request.POST:
                if request.POST['new_worker'] != '':
                    full_name = request.POST['new_worker'].split(' ',1)
                    worker = Worker.objects.filter(first_name__contains=full_name[1], last_name__contains=full_name[0])
                    ticket.ticket_worker = worker.get()
            if 'new_content' in request.POST:
                if request.POST['new_content'] != '':
                    ticket.ticket_content = request.POST['new_content']
            ticket.save()
            context['ticket'] = ticket
            return HttpResponseRedirect(reverse('base:ticket_detail', args=[ticket_id]))


@login_required(login_url=login_page)
def ticket_summary(request, summary_filter=None, summary_sort=None):
    if request.user.is_staff or request.user.groups.first().id == 2:
        obj_str = ObjStr.objects.order_by('street')
        date_now = timezone.now().astimezone().strftime("%Y-%m-%d")
        obj_managecomp = ManageComp.objects.order_by('comp_name')
        area_list = ObjArea.objects.order_by('area_name')
        status_list = TicketStatus.objects.all();
        first_date = Ticket.objects.first().ticket_date.date()
        context = {
            'date_now': date_now,
            'obj_str': obj_str,
            'manage_comp': obj_managecomp,
            'area_list': area_list,
            'status_list': status_list,
            'first_date': first_date,
        }
        if request.method == 'GET':
            context.update({
                'obj_build':'None',
                'obj_buildhousing':'None',
                'obj_type':'None',
                'obj_par':'None',
            })
            return render(request, 'base/summary.html', context)

        if request.method == 'POST':

#Summary by Obj_managecomp and time period--

            if summary_filter == 'address':
                new_objbuildhousing = None
                new_objpar = None
                new_objtype = None
#--obj filters
                filter_context = Object.objects.all()
                ticket_filter = Ticket.objects.filter(ticket_object = None)

#--manage_comp handler

                if 'manage_comp' in request.POST:
                    if request.POST['manage_comp'] != '':
                        ticket_filter.filter()

                        obj_list = Object.objects.filter(obj_str__in = [ticket.ticket_str for ticket in ticket_filter], obj_build__in = [ticket.ticket_build for ticket in ticket_filter]).filter(manage_comp__comp_name = request.POST['manage_comp']) #Список подходящих объектов для открытых заявок, составленный по всем заявкам без прикрепленных объектов и фильтрованный по выбранной управляющей компании
                        ticket_filter = ticket_filter.filter(ticket_str__in = [obj.obj_str for obj in obj_list], ticket_build__in = [obj.obj_build for obj in obj_list]) #Список открытых заявок соответствующих выбранной управляющей компании

                        filter_context = filter_context.filter(manage_comp__comp_name = request.POST['manage_comp'])
                        context['obj_managecomp'] = request.POST['manage_comp']
                        obj_str = obj_str.filter(street__in=[obj.obj_str for obj in filter_context])
                        context.update({
                            'obj_str': obj_str,
                        })

#--obj_str handler

                if 'obj_str' in request.POST:
                    if request.POST['obj_str'] == '':
                        context['help_message'] = ""
                    else:
                        try:
                            new_objstr = ObjStr.objects.get(street=request.POST['obj_str'])
                        except(KeyError, ObjStr.DoesNotExist):
                            context['error_message'] = "Значение улицы не заполнено"
                        except(KeyError, MultiValueDictKeyError):
                            context['error_message'] = "Улица не выбрана"
                        else:
                            context['str_value'] = new_objstr
                            filter_context = filter_context.filter(obj_str = new_objstr)
                            ticket_filter = ticket_filter.filter(ticket_str__street = new_objstr)
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
                            filter_context = filter_context.filter(obj_build = new_objbuild)
                            ticket_filter = ticket_filter.filter(ticket_build =  new_objbuild)

#--obj_build_housing check for exists

                obj_buildhousing = filter_context.values('obj_build_housing').order_by('obj_build_housing').distinct() #--obj_buildhousing filtered datalist

                if obj_buildhousing.count()>0:
                    if obj_buildhousing[0]['obj_build_housing'] == None:
                        context['obj_buildhousing'] = None
                    else:
                        context['obj_buildhousing'] = obj_buildhousing


#--obj_build_housing handler

                if 'obj_buildhousing' in context:
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
                                    filter_context = filter_context.filter(obj_build_housing = new_objbuildhousing)
                                    ticket_filter = ticket_filter.filter(ticket_build_housing = new_objbuildhousing)
                    else:
                        new_objbuildhousing = None

#--obj_par check for exists

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
                                filter_context = filter_context.filter(obj_par = new_objpar)
                                ticket_filter = ticket_filter.filter(ticket_par = new_objpar)
                            context['par_value'] = new_objpar


#--obj_type check for exists

                obj_type = filter_context.values('obj_type').order_by('obj_type').distinct()	#obj_type filtered datalist
                if obj_type.count()>0:
                    if obj_type[0]['obj_type'] == None:
                        context['obj_type'] = None
                    else:
                        context['obj_type'] = ObjType.objects.filter(pk__in=obj_type)

#--obj_type handler

                if 'obj_type' in request.POST:
                    if request.POST['obj_type'] == '':
                        context['help_message'] = "Выберите тип лифта"
                    else:
                        try:
                            new_objtype = ObjType.objects.get(type_name=request.POST['obj_type'])
                        except(KeyError, ObjType.DoesNotExist):
                            context['error_message'] = "Значение типа лифта не верно"
                        else:
                            filter_context = filter_context.filter(obj_type__type_name = new_objtype)
                            ticket_filter = ticket_filter.filter(ticket_obj_type__type_name = new_objtype)


                if 'ticket_date_start' in request.POST:
                    ticket_date_start = request.POST['ticket_date_start']
                    context['date_start'] = ticket_date_start
                else:
                    ticket_date_start = first_date

                if 'ticket_date_end' in request.POST:
                    ticket_date_end = request.POST['ticket_date_end']
                    context['date_end'] = ticket_date_end
                else:
                    ticket_date_end = timezone.now().astimezone()


                if 'declineact' in request.POST:
                    if request.POST['declineact'] == 'on':
                        context['declineact'] = True

#--rerender form for ajax

                if 'sender' in request.POST:
                    if request.POST['sender'] == 'jQuery':
                        return render(request, 'base/summary.html', context)

                ticket_summary = Ticket.objects.filter(ticket_date__range=(ticket_date_start,ticket_date_end))

#--manage_comp filter

                if 'manage_comp' in request.POST:
                    if request.POST['manage_comp'] != '':
                        context['obj_managecomp'] = request.POST['manage_comp']
                        filter_context = filter_context.filter(manage_comp__comp_name = request.POST['manage_comp'])

#--obj_address filter

                ticket_summary = ticket_summary.filter(Q(ticket_object__in = [obj.id for obj in filter_context]) | Q(id__in = [t.id for t in ticket_filter])).order_by('ticket_date__year', 'ticket_date__month', 'ticket_date__day', 'ticket_str')

#--decline_act filter

                if 'declineact' in request.POST:
                    if request.POST['declineact'] == 'on':
                        context['declineact'] = True
#                        ticket_summary = ticket_summary.filter(Q(ticket_duration__gte = timezone.timedelta( days = 1 )) | Q(ticket_duration = None)) #!--Тестовое ограничение
                        for ticket in ticket_summary:
                            if ticket.ticket_object != None:
                                if ticket.ticket_duration != None:
                                    if ticket.ticket_object.manage_comp != None:
                                        if ticket.ticket_duration < ticket.ticket_object.manage_comp.decline_period:
                                            ticket_summary = ticket_summary.exclude(id = ticket.id)
                                    else:
                                        ticket_summary = ticket_summary.exclude(id = ticket.id)
                                else:
                                    if ticket.ticket_object.manage_comp != None:
                                        if ticket.ticket_date > (timezone.now().astimezone() - ticket.ticket_object.manage_comp.decline_period):
                                            ticket_summary = ticket_summary.exclude(id = ticket.id)
                                    else:
                                        ticket_summary = ticket_summary.exclude(id = ticket.id)
                            else:
                                obj_list = Object.objects.filter(obj_str = ticket.ticket_str, obj_build = ticket.ticket_build, obj_build_housing = ticket.ticket_build_housing, obj_par = ticket.ticket_par)
                                if ticket.ticket_date > (timezone.now().astimezone() - obj_list[0].manage_comp.decline_period):
                                    ticket_summary = ticket_summary.exclude(id = ticket.id)

                context['ticket_summary'] = ticket_summary

                if 'csv_checker' in request.POST:
                    if request.POST['csv_checker'] == 'on':

                        response = HttpResponse(content_type='text/csv', charset="1251")
                        response['Content-Disposition'] = 'attachment; filename="summary_address_%s.csv"' % (timezone.now().strftime('%d.%m.%Y %H:%M:%S'))

                        writer = csv.writer(response, dialect='excel', delimiter=';')
                        writer.writerow(['Открыта','Закрыта','Продолжительность','Район','Улица','Строение','Корпус','Парадная','Тип лифта','Содержание заявки'])
                        for ticket in ticket_summary:
                            if ticket.close_time:
                                close_time = ticket.close_time.strftime('%d.%m.%Y %H:%M:%S')
                            else:
                                close_time = ''
                            writer.writerow([ticket.ticket_date.strftime('%d.%m.%Y %H:%M:%S'),close_time,ticket.duration_time,ticket.ticket_str.area,ticket.ticket_str,ticket.ticket_build,ticket.ticket_build_housing,ticket.ticket_par,ticket.ticket_obj_type,ticket.ticket_content])

                        return response

                return render(request, 'base/summary.html', context)

#Summary by ticket_area and one day--

        if summary_filter == 'area':

            if 'tickets_area' in request.POST:
                if request.POST['tickets_area'] != '':
                    new_area = request.POST['tickets_area']
                    context['tickets_area'] = new_area
                    ticket_summary = Ticket.objects.filter(ticket_str__area__area_name = new_area)

            if 'area_tickets_date' in request.POST:
                if request.POST['area_tickets_date'] != '':
                    new_date = request.POST['area_tickets_date']
                    context['area_tickets_date'] = new_date
                    if 'tickets_area' in request.POST:
                        if request.POST['tickets_area'] != '':
                            ticket_summary = ticket_summary.filter(ticket_date__date = new_date)
                        else:
                            ticket_summary = Ticket.objects.filter(ticket_date__date = new_date).order_by('ticket_str__area', 'ticket_date')

            context['ticket_summary'] = ticket_summary

            if 'csv_checker' in request.POST:
                if request.POST['csv_checker'] == 'on':
                    response = HttpResponse(content_type='text/csv', charset="1251")
                    response['Content-Disposition'] = 'attachment; filename="summary_area_%s.csv"' % (timezone.now().strftime('%d.%m.%Y %H:%M:%S'))

                    writer = csv.writer(response, dialect='excel', delimiter=';')
                    writer.writerow(['Открыта','Закрыта','Продолжительность','Район','Улица','Строение','Корпус','Парадная','Тип лифта','Содержание заявки'])
                    for ticket in ticket_summary:
                        if ticket.close_time:
                            close_time = ticket.close_time.strftime('%d.%m.%Y %H:%M:%S')
                        else:
                            close_time = ''
                        writer.writerow([ticket.ticket_date.strftime('%d.%m.%Y %H:%M:%S'),close_time,ticket.duration_time,ticket.ticket_str.area,ticket.ticket_str,ticket.ticket_build,ticket.ticket_build_housing,ticket.ticket_par,ticket.ticket_obj_type,ticket.ticket_content])

                    return response

            return render(request, 'base/summary.html', context)

#Summary by ticket_status and time period--

        if summary_filter == 'status':

            statuses = [];

            for tickets_status in TicketStatus.objects.all():
                if str(tickets_status.id) in request.POST:
                    statuses.append(tickets_status.status)

            context['statuses'] = statuses

            ticket_summary = Ticket.objects.filter(ticket_status__status__in = statuses).order_by('ticket_str__area','ticket_date')

            if 'status_date_start' in request.POST:
                status_date_start = request.POST['status_date_start']
                context['status_date_start'] = status_date_start
            else:
                status_date_start = Ticket.objects.first().ticket_date.date()

            if 'status_date_end' in request.POST:
                status_date_end = request.POST['status_date_end']
                context['status_date_end'] = status_date_end
            else:
                status_date_end = timezone.now().astimezone()

            context['ticket_summary'] = ticket_summary

            if 'csv_checker' in request.POST:
                if request.POST['csv_checker'] == 'on':
                    response = HttpResponse(content_type='text/csv', charset="1251")
                    response['Content-Disposition'] = 'attachment; filename="summary_status_%s.csv"' % (timezone.now().strftime('%d.%m.%Y %H:%M:%S'))

                    writer = csv.writer(response, dialect='excel', delimiter=';')
                    writer.writerow(['Открыта','Закрыта','Простой','Район','Улица','Строение','Корпус','Парадная','Тип лифта','Причина'])
                    for ticket in ticket_summary:
                        if ticket.close_time:
                            close_time = ticket.close_time.strftime('%d.%m.%Y %H:%M:%S')
                        else:
                            close_time = ''
                        writer.writerow([ticket.ticket_date.strftime('%d.%m.%Y %H:%M:%S'),close_time,ticket.duration_get(),ticket.ticket_str.area,ticket.ticket_str,ticket.ticket_build,ticket.ticket_build_housing,ticket.ticket_par,ticket.ticket_obj_type,ticket.ticket_content])

                    return response

            return render(request, 'base/summary.html', context)