from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ticket.models import Ticket, Developer
import json    
import re
from lib.ticket_processing_helper import *

status = {'Open': 3, 'Working': 2, 'Closed': 1}
priority = {'Now': 3, 'Soon': 2, 'Someday': 1}

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
    fetch = json.loads(request.body)['fetch']
    if fetch == 'all':
        tickets = Ticket.objects.all().values()
    else:
        tickets = Ticket.objects.filter(assigned_to = request.user).values()
    tickets = make_json_dict(normalize_tickets(tickets))
    return HttpResponse(content = json.dumps(tickets), content_type = "application/json; charset=UTF-8")

def sort_tickets(request):
    pass    
