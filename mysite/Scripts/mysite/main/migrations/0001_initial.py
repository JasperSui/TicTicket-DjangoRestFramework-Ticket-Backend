# Generated by Django 2.1.7 on 2019-03-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('number_of_people', models.CharField(blank=True, max_length=45, null=True)),
                ('key', models.CharField(blank=True, max_length=45, null=True)),
                ('total_price', models.CharField(blank=True, max_length=45, null=True)),
                ('buy_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ticket',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('begin_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('number_of_seat', models.IntegerField()),
                ('remaining_seat', models.IntegerField()),
            ],
            options={
                'db_table': 'ticket_type',
                'managed': False,
            },
        ),
    ]
