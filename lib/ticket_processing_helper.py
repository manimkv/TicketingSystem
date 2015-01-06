from datetime import datetime
from django.contrib.auth.models import User

def normalize_tickets(tickets):
    for ticket in tickets:
    	single_ticket = {}
        ticket['submitted_date'] = ticket['submitted_date'].strftime('%Y-%m-%d %H:%m')
        ticket['modified_date'] = ticket['modified_date'].strftime('%Y-%m-%d %H:%m')
        ticket['first_response'] = ticket['first_response'].strftime('%Y-%m-%d %H:%m') if ticket['first_response'] else ticket['first_response']
        ticket['contact'] = str(User.objects.get(id = ticket.pop('contact_id')))
        ticket['assigned_to'] = str(User.objects.get(id = ticket.pop('assigned_to_id')))
    return tickets    

def make_json_dict(tickets):
    return dict(map(lambda t: (t['id'], t), tickets))