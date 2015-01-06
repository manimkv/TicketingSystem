from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from ticket.models import Ticket, Developer
import json    
import re
from lib.ticket_processing_helpers import *
from datetime import datetime
from calendar import monthrange


def signin(request):
    return render(request, 'signin.html')

def login_view(request):
    data = json.loads(request.body)
    EMAIL_user = User.objects.filter(email = data['email'])
    USERNAME_user = User.objects.filter(username = data['email'])
    USER = EMAIL_user if EMAIL_user else USERNAME_user
    if USER:
        USER = USER[0]
        user = authenticate(username = USER.username , password = data['password'])
        if user:
            login(request, user)
            response = "succesfull"
        else:
            response = "authentication failed"
    else:
        response = "user not registered"
    return HttpResponse(content = json.dumps(response), content_type = "application/json; charset=UTF-8")

def logout_view(request):
    logout(request)
    return render(request, 'signin.html')

@login_required
def dashboard(request):
    logged_user = str(request.user)
    if logged_user == 'admin':
    	response = 'admin_dashboard.html'
    else:
    	response = 'developer_dashboard.html'
    return render(request, response, {'username': logged_user})

@login_required
def fetch_tickets(request):
    sort_parm = request.GET['sort_parm']
    if str(request.user) == 'Admin':
        tickets = Ticket.objects.all().values()
    else:
        tickets = Ticket.objects.filter(assigned_to = request.user).values()
    tickets = get_sorted_tickets(normalize_tickets(tickets), parm = sort_parm)
    return HttpResponse(content = json.dumps(tickets), content_type = "application/json; charset=UTF-8")

def search_tickets(request):
    query = request.GET['query']
    tickets = Ticket.objects.filter(Q(subject__icontains = query) | Q(description__icontains = query) | Q(status__icontains = query) | Q(priority__icontains = query)).values()
    tickets = get_sorted_tickets(normalize_tickets(tickets))
    return HttpResponse(content = json.dumps(tickets), content_type = "application/json; charset=UTF-8")

def filter_tickets(request):
    query = request.GET['filter_parm']
    if str(request.user) == 'Admin':
        filtered_tickets = Ticket.objects.filter(Q(status = query) | Q(priority = query)).values()
    else:
        filtered_tickets = Ticket.objects.filter(Q(status = query) | Q(priority = query), assigned_to = request.user).values()    
    tickets = get_sorted_tickets(normalize_tickets(filtered_tickets), parm = 'priority')       
    return HttpResponse(content = json.dumps(tickets), content_type = "application/json; charset=UTF-8")

def ticket_action(request):
    data = json.loads(request.body)
    action, _id = data['action'], data['id']
    if action == 'new':
        ticket = data['ticket']
        response = 'Ticket Created Succesfully'
        try:
            Ticket.objects.create(subject = ticket['subject'],
                                  contact = User.objects.get(username = ticket['contact']),
                                  assigned_to = User.objects.get(username = ticket['assigned_to']),
                                  description = ticket.get('description', ''),
                                  status = ticket.get('status', 'Open'),
                                  priority = ticket.get('priority', 'Now'))
        except (KeyError, IntegrityError) as e:
            response = e.__class__.__name__
    elif action == 'update':
        ticket = Ticket.objects.get(id = _id)
        response = 'Ticket Updated Succesfully'
    else:
        Ticket.objects.get(id = _id).delete()
        response = 'Ticket Deleted Succesfully'
    return HttpResponse(content = json.dumps(response), content_type = "application/json; charset=UTF-8")

@login_required
def add_developer(request):
    data = json.loads(request.body)
    try:
        response = 'Developer Created Succesfully'
        user = User.objects.create(username = data['username'],
                                   email = data['email'],
                                   first_name = data['first_name'],
                                   last_name = data.get('last_name', '')
                                   )   
        user.set_password(data['password'])
        user.save()        
        Developer.objects.create(user=User.objects.get(username = data['username']),
                                 mobile = data['mobile'])
    except IntegrityError:
        response = 'Developer Already Exists'    
    return HttpResponse(content=json.dumps(response), content_type='application/json')    

def avg_closed(request):
    data = json.loads(request.body)
    month, year = data.month('month', ''), data['year']
    if month:
        start_date = datetime.strptime('%s%s01' % (year, '0%s' % month if month<10 else month) , '%Y%m%d')
        end_date = datetime.strptime('%s%s%s' % (year,  '0%s' % month if month<10 else month, monthrange(year, month)[1]) , '%Y%m%d')
    else:
        start_date = datetime.strptime('%s0101' % year , '%Y%m%d')
        start_date = datetime.strptime('%s1231' % year, '%Y%m%d')
    available_tickets = Ticket.objects.filter(submitted_date__range = (start_date, end_date))
    