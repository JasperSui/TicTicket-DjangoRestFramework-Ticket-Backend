# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import Bit1BooleanField

class User(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    money = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Session(models.Model):
    expire_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'session'


class TempTicket(models.Model):
    user_email = models.CharField(max_length=255)
    ticket_type = models.ForeignKey('TicketType', models.DO_NOTHING)
    number_of_people = models.IntegerField()
    key = models.CharField(max_length=45, blank=True, null=True)
    total_price = models.IntegerField()
    buy_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_ticket'

    
class Ticket(models.Model):
    user_email = models.CharField(max_length=255)
    ticket_type = models.ForeignKey('TicketType', models.DO_NOTHING)
    number_of_people = models.IntegerField()
    key = models.CharField(max_length=45, blank=True, null=True)
    total_price = models.IntegerField()
    buy_time = models.DateTimeField(blank=True, null=True)
    is_used = Bit1BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketType(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    show_time = models.DateTimeField(blank=True, null=True)
    number_of_seat = models.IntegerField()
    remaining_seat = models.IntegerField()
    image_url = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'ticket_type'
