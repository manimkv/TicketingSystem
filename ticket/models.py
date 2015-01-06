
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
    (1, 'Open'),
    (2, 'Working'),
    (3, 'Closed'),
    )

PRIORITY_CODES = (
    (1, 'Now'),
    (2, 'Soon'),
    (3, 'Someday'),
    )

class Ticket(models.Model):
    subject = models.CharField(max_length = 100)
    submitted_date = models.DateField(auto_now_add = True)
    modified_date = models.DateField(auto_now = True)
    first_response = models.DateField(blank = True, null = True)
    contact = models.ForeignKey(User, related_name = "who raised")
    assigned_to = models.ForeignKey(User)
    description = models.TextField(blank = True, null = True)
    status = models.IntegerField(default = 1, choices = STATUS_CODES)
    priority = models.IntegerField(default = 1, choices = PRIORITY_CODES)

    def __str__(self):
        return self.subject
