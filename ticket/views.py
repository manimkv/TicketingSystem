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
    return HttpResponse(content = json.dumps("Logout Succesfully"), content_type = "application/json; charset=UTF-8")

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
    fetch_for = 'all' if str(request.user) == 'Admin' else None
    if fetch_for == 'all':
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

