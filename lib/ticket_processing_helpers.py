from datetime import datetime
from django.contrib.auth.models import User
from collections import defaultdict
from operator import itemgetter

def normalize_tickets(tickets):
    for ticket in tickets:
    	single_ticket = {}
        ticket['submitted_date'] = ticket['submitted_date'].strftime('%Y-%m-%d %H:%m')
        ticket['modified_date'] = ticket['modified_date'].strftime('%Y-%m-%d %H:%m')
        ticket['first_response'] = ticket['first_response'].strftime('%Y-%m-%d %H:%m') if ticket['first_response'] else ticket['first_response']
        ticket['contact'] = str(User.objects.get(id = ticket.pop('contact_id')))
        ticket['assigned_to'] = str(User.objects.get(id = ticket.pop('assigned_to_id')))
    return tickets    

def get_sorted_tickets(tickets, parm = 'status'):
    status, priority = {'Open': 1, 'Working': 2, 'Closed': 3}, {'Now': 1, 'Soon': 2, 'Someday': 3}
    key = lambda y: y[parm]
    if parm in ['status', 'priority']:
        parm_dict = eval(parm)
        key = lambda y: parm_dict[y[parm]]
    return sorted(tickets, key = key)
