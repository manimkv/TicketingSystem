# import memcache
# from TicketSysytem.settings import MEMCACHE
# mc = memcache.Client(['%s:%s'%(MEMCACHE['host'], MEMCACHE['port'])], debug=0)

# def populate_memcache():
#     for ticket in tickets:
#     	single_ticket = {}
#         ticket['submitted_date'] = ticket['submitted_date'].strftime('%Y-%m-%d %H:%m')
#         ticket['modified_date'] = ticket['modified_date'].strftime('%Y-%m-%d %H:%m')
#         ticket['first_response'] = ticket['first_response'].strftime('%Y-%m-%d %H:%m') if ticket['first_response'] else ticket['first_response']
#         ticket['contact'] = str(User.objects.get(id = ticket.pop('contact_id')))
#         ticket['assigned_to'] = str(User.objects.get(id = ticket.pop('assigned_to_id')))
#         res_tickets[ticket['id']] = ticket
    # return res_tickets    	