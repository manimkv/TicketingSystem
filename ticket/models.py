
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields = ['last_login'])
    user_logged_in.connect(update_last_login)

class Developer(models.Model):  
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length = 20)
    last_login = models.DateTimeField(default = timezone.now)
    
    def __unicode__(self):
        return unicode(self.user)

STATUS_CODES = (
    ('Open', 'Open'),
    ('Working', 'Working'),
    ('Closed', 'Closed'),
    )

PRIORITY_CODES = (
    ('Now', 'Now'),
    ('Soon', 'Soon'),
    ('Someday', 'Someday'),
    )

class Ticket(models.Model):
    subject = models.CharField(max_length = 100, unique = True)
    submitted_date = models.DateField(default = timezone.now)
    modified_date = models.DateField(default = timezone.now)
    first_response = models.DateField(blank = True, null = True)
    contact = models.ForeignKey(User, related_name = "who raised")
    assigned_to = models.ForeignKey(User)
    description = models.TextField(blank = True, null = True)
    status = models.CharField(default = 'Open', max_length = 10, choices = STATUS_CODES)
    priority = models.CharField(default = 'Now', max_length = 10, choices = PRIORITY_CODES)

    def __str__(self):
        return self.subject
