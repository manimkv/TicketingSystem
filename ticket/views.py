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
from lib.utils import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
    if logged_user == 'Admin':
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
    action, _id, ticket = data['action'], data['id'], data.get('ticket', {})
    if action == 'new':
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
        t = Ticket.objects.get(id = _id)
        t.status = ticket['status']
        if not tictket.first_response:
            t.first_response = ticket['first_response']
        t.save()
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

def avg_closed_tickets(request):
    data = json.loads(request.body)
    month, year, for_all = data.get('month', ''), data['year'], data['for_all']
    start_date, end_date = get_relative_dates(month, year)
    if for_all:
        available_tickets = Ticket.objects.filter(submitted_date__range = (start_date, end_date))
        closed_tickets = Ticket.objects.filter(submitted_date__range = (start_date, end_date), status = 'Closed')
    else:
        user = User.objects.get(username = data['username'])
        available_tickets = Ticket.objects.filter(assigned_to = user, submitted_date__range = (start_date, end_date))
        closed_tickets = Ticket.objects.filter(assigned_to = user, submitted_date__range = (start_date, end_date), status = 'Closed')        
    try:
        len_closed_tickets, len_available_tickets = len(closed_tickets), len(available_tickets)
        avg_closed = (float(len_closed_tickets) / float(len_available_tickets)) * 100
    except ZeroDivisionError:
        avg_closed = 0.0
    response = {'available_tickets': len_available_tickets, 'closed_tickets': len_closed_tickets, 'avg_closed': avg_closed}
    return HttpResponse(content=json.dumps(response), content_type='application/json')    

def avg_response_tickets(request):
    data = json.loads(request.body)
    month, year, for_all = data.get('month', ''), data['year'], data['for_all']
    start_date, end_date = get_relative_dates(month, year)
    if for_all:
        available_tickets = Ticket.objects.filter(submitted_date__range = (start_date, end_date))
    else:
        user = User.objects.get(username = data['username'])
        available_tickets = Ticket.objects.filter(assigned_to = user, submitted_date__range = (start_date, end_date))
    without_response = with_response = sum_dif = 0 
    for t in available_tickets:
        if t.first_response:
            sum_dif += (t.first_response - t.submitted_date).total_seconds()
            with_response += 1
        else:
            without_response += 1
    try:
        avg_response = float(sum_dif) / float(with_response) * 3600.0
    except ZeroDivisionError:
        avg_response = 0
    response = {'without_response': without_response, 'with_response': with_response, 'avg_response': avg_response}
    return HttpResponse(content=json.dumps(response), content_type='application/json')    

