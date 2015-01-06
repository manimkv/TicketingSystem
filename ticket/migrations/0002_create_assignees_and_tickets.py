# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from ticket.models import Developer, Ticket
from random import randrange
from datetime import datetime, timedelta

class Migration(DataMigration):

    def random_date(self, start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 3600) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds = random_second)

    def forwards(self, orm):
        "Write your forwards methods here."
        ### creating assignees
        assignees = [{'username': 'developer1', 'password': 'developer1', 'email': 'developer1@gmail.com', 'first_name': 'dev1', 'mobile': 9999999991},
                     {'username': 'developer2', 'password': 'developer2', 'email': 'developer2@gmail.com', 'first_name': 'dev2', 'mobile': 9999999992},
                     {'username': 'developer3', 'password': 'developer3', 'email': 'developer3@gmail.com', 'first_name': 'dev3', 'mobile': 9999999993},
                     {'username': 'developer4', 'password': 'developer4', 'email': 'developer4@gmail.com', 'first_name': 'dev4', 'mobile': 9999999994},
                     {'username': 'developer5', 'password': 'developer5', 'email': 'developer5@gmail.com', 'first_name': 'dev5', 'mobile': 9999999995},
                     {'username': 'developer6', 'password': 'developer6', 'email': 'developer6@gmail.com', 'first_name': 'dev6', 'mobile': 9999999996},
                     {'username': 'developer7', 'password': 'developer7', 'email': 'developer7@gmail.com', 'first_name': 'dev7', 'mobile': 9999999997},
                     {'username': 'developer8', 'password': 'developer8', 'email': 'developer8@gmail.com', 'first_name': 'dev8', 'mobile': 9999999998},
                     {'username': 'developer9', 'password': 'developer9', 'email': 'developer9@gmail.com', 'first_name': 'dev9', 'mobile': 9999999999},
                     {'username': 'developer0', 'password': 'developer0', 'email': 'developer0@gmail.com', 'first_name': 'dev0', 'mobile': 9999999990}]
        
        for assignee in assignees:
            user = User.objects.create(username = assignee['username'],
                                       email = assignee['email'],
                                       first_name = assignee['first_name'],
                                       last_name = '')
            user.set_password(assignee['password'])
            user.save()
            Developer.objects.create(user = User.objects.get(username = assignee['username']),
                                     mobile = assignee['mobile'])
        
        ### ticket creation
        _from, _to = datetime.strptime('20150101', '%Y%m%d'), datetime.strptime('20151212', '%Y%m%d')
        users = User.objects.filter(~Q(username = 'Admin'))
        STATUS, PRIORITY = ['Open', 'Working', 'Closed'], ['Now', 'Soon', 'Someday']
        
        for i in range(5000):
            subject = 'issue00%s' % i
            submitted_date = self.random_date(_from, _to)
            first_response = self.random_date(submitted_date, _to) 
            modified_date = self.random_date(first_response, _to)
            contact = users[randrange(len(users))]
            rest = [u for u in users if u != contact]
            assigned_to = rest[randrange(len(rest))]
            description = 'description00%s' % i
            status = STATUS[randrange(3)]
            priority = PRIORITY[randrange(3)]

            Ticket.objects.create(subject = subject,
                                  submitted_date = submitted_date,
                                  first_response = first_response,
                                  modified_date = modified_date,
                                  contact = contact,
                                  assigned_to = assigned_to,
                                  description = description,
                                  status = status,
                                  priority = priority)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ticket.developer': {
            'Meta': {'object_name': 'Developer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'ticket.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'who raised'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_response': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'Now'", 'max_length': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '10'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'submitted_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ticket']
    symmetrical = True
