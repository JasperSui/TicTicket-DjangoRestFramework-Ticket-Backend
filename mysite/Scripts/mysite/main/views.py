from main.models import TempTicket, Ticket, TicketType, User
from main.serializers import TempTicketSerializer, TicketSerializer, TicketTypeSerializer, UserSerializer
from common.Ticket import *
from django.shortcuts import get_object_or_404
from django.core import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import *
import pytz, datetime, pdb, json, uuid, random, string

# Create your views here.
class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

    # @detail_route(methods=['get'], url_path='get-specific-ticket-type')
    # def get_specific_ticket_type(self,request,pk=None):

    #     data = serializers.serialize('json', TicketType.objects.get(pk=pk))

    #     return JsonResponse(data, status=200,safe=False)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request):

        data = request.data

        user_email = data.get('user_email')
        ticket_type_id = data.get('ticket_type_id')
        number_of_people = data.get('number_of_people')
        key = GenerateKeyByTicketTypeId(int(ticket_type_id))
        buy_time_string = data.get('buy_time')
        buy_time = datetime.datetime.strptime(buy_time_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)
        total_price = number_of_people * ticket_type.price
        ticket = TempTicket.objects.create(
            user_email=user_email,
            ticket_type_id=ticket_type_id,
            number_of_people=number_of_people,
            key=key,
            total_price=total_price,
            buy_time=buy_time
            )

        ticket_object = get_object_or_404(TempTicket, pk=ticket.id)
        user = User.objects.get(email=user_email)
        former_money = user.money
        if former_money >= total_price:
            latter_money = former_money - total_price
            user.money = latter_money
            user.save()
            update_result = UpdateTicketTypeRemainingSeat(ticket_type, number_of_people)
            if update_result:
                return JsonResponse({'status':"success", "ticket_key": key}, status=201)
            else:
                return JsonResponse({'status':"failed"}, status=400)
        else:
            return JsonResponse({'status':"failed"}, status=400)


class TempTicketViewSet(viewsets.ModelViewSet):
    queryset = TempTicket.objects.all()
    serializer_class = TempTicketSerializer

    def create(self, request):

        data = request.data

        user_email = data.get('user_email')
        ticket_type_id = data.get('ticket_type_id')
        number_of_people = data.get('number_of_people')
        key = GenerateKeyByTicketTypeId(int(ticket_type_id))
        buy_time_string = data.get('buy_time')
        buy_time = datetime.datetime.strptime(buy_time_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)

        ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)
        ticket = TempTicket.objects.create(
            user_email=user_email,
            ticket_type_id=ticket_type_id,
            number_of_people=number_of_people,
            key=key,
            total_price=number_of_people*ticket_type.price,
            buy_time=buy_time
            )

        ticket_object = get_object_or_404(TempTicket, pk=ticket.id)

        user = User.objects.get(email=user_email)
        user.money = user.money - number_of_people * ticket_type.price
        user.save()

        return JsonResponse({'status':"success"}, status=201)

    @list_route(methods=['post'], url_path='get-user-temp-ticket-price-and-key')
    def get_user_temp_ticket_price_and_key(self, request):

        data = request.data
        user_email = data.get('user_email')
        temp_ticket = TempTicket.objects.get(user_email=user_email)

        return JsonResponse({'price': temp_ticket.total_price, 'key': temp_ticket.key}, status=200)

    @list_route(methods=['post'], url_path='transfer-ticket-data-to-formal-table')
    def transfer_ticket_data_to_formal_table(self, request):

        data = request.data

        user_email = data.get('user_email')
        temp_ticket = TempTicket.objects.get(user_email=user_email)
        ticket_type = get_object_or_404(TicketType, pk=temp_ticket.ticket_type_id)
        ticket = Ticket.objects.create(
            user_email=temp_ticket.user_email,
            ticket_type_id=temp_ticket.ticket_type_id,
            number_of_people=temp_ticket.number_of_people,
            key=temp_ticket.key,
            total_price=temp_ticket.total_price,
            buy_time=temp_ticket.buy_time
            )
        ticket_object = get_object_or_404(Ticket, pk=ticket.id)
        update_result = UpdateTicketTypeRemainingSeat(ticket_type, temp_ticket.number_of_people)
        TempTicket.objects.filter(user_email=user_email).delete()

        if update_result and TempTicket.objects.filter(user_email=user_email).count() == 0 and Ticket.objects.filter(key=temp_ticket.key).count() > 0:

            return JsonResponse({'status':"success"}, status=201)

        else:

            return JsonResponse({'status':"failed"}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #註冊函數
    def create(self, request):

        data = request.data

        email = data.get('email')
        unencrypt_password  = data.get('password')
        name = data.get('name')
        birthday = datetime.datetime.strptime(data.get('birthday'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)

        if User.objects.filter(email=email).count() > 0:

            return JsonResponse({'status':"failed"}, status=400)

        user = User.objects.create(
            email=email,
            password=make_password(unencrypt_password),
            name=name,
            birthday=birthday
            )

        user_object = get_object_or_404(User, email=email)

        if isinstance(user_object, User):

            return JsonResponse({'status':"success"}, status=201)

        else:

            return JsonResponse({'status':"failed"}, status=400)

    @list_route(methods=['post'])
    def login(self, request):

        data = request.data

        email = data.get('email')
        unencrypt_password  = data.get('password')

        user = User.objects.get(email=email)

        if check_password(unencrypt_password, user.password):

            return JsonResponse({'status':"success"}, status=200)

        else:

            return JsonResponse({'status':"failed"}, status=400)

    @list_route(methods=['post'])
    def deposit(self, request):

        data = request.data

        email = data.get('user_email')
        money = data.get('money')

        user = User.objects.get(email=email)

        former_money = user.money
        latter_money = former_money + money
        user.money = latter_money
        user.save()

        if user.money == latter_money:

            return JsonResponse({'status':"success", "money": latter_money}, status=200)

        else:

            return JsonResponse({'status':"failed"}, status=400)

    @list_route(methods=['post'])
    def debit(self, request):

        data = request.data

        email = data.get('user_email')
        money = data.get('money')

        user = User.objects.get(email=email)

        former_money = user.money
        latter_money = former_money - money
        user.money = latter_money
        user.save()

        if user.money == latter_money:

            return JsonResponse({'status':"success", "money": latter_money}, status=200)

        else:

            return JsonResponse({'status':"failed"}, status=400)

    @list_route(methods=['post'])
    def change_password(self, request):

        data = request.data

        email = data.get('user_email')
        unencrypt_password = data.get('password')
        user = User.objects.get(email=email)
        user.password = make_password(unencrypt_password)
        user.save()

        if check_password(unencrypt_password, user.password):

            return JsonResponse({'status': "success"}, status=200)

        else:

            return JsonResponse({'status': "failed"}, status=400)

    @list_route(methods=['post'])
    def edit_profile(self, request):

        data = request.data

        email = data.get('user_email')
        name = data.get('name')
        birthday = datetime.datetime.strptime(
            data.get('birthday'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        address = data.get('address')
        telephone = data.get('telephone')

        user = User.objects.get(email=email)

        user.name = name
        user.birthday = birthday
        user.address = address
        user.telephone = telephone
        user.save()
        update_result = (user.name == name) and (user.birthday == birthday) and (user.address == address) and (user.telephone == telephone)
        
        if update_result:

            return JsonResponse({'status': "success"}, status=200)

        else:

            return JsonResponse({'status': "failed"}, status=400)

    @list_route(methods=['post'], url_path='get-user-info-by-email')
    def get_user_info_by_email(self, request):

        data = request.data

        email = data.get('email')

        user = User.objects.filter(email=email)
        serializer = UserSerializer(user, many=True)

        return JsonResponse(serializer.data[0])

def GenerateKeyByTicketTypeId(ticket_type_id):
    split_number_list = list()
    while ticket_type_id > 0:
        temp = random.randint(0, ticket_type_id)
        split_number_list.append(temp)
        ticket_type_id -= temp
    temp_key_list = list(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=20-len(split_number_list))))
    for number in split_number_list:
        temp1 = random.randint(0, len(temp_key_list))
        temp_key_list.insert(temp1, str(number))
    return ''.join(temp_key_list)
