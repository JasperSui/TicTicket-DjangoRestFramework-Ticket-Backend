from rest_framework import serializers
from main.models import TempTicket, Ticket, TicketType, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'birthday', 'address', 'telephone', 'money')
            

class TicketSerializer(serializers.ModelSerializer):
    model = Ticket
    show_time = serializers.SerializerMethodField()

    def get_show_time(self, obj):
        return obj.ticket_type.show_time

    class Meta:
        model = Ticket
        # fields = '__all__'
        fields = ('id', 'ticket_type_id', 'number_of_people', 'key', 'total_price', 'show_time', 'buy_time')


class TempTicketSerializer(serializers.ModelSerializer):
    model = TempTicket
    show_time = serializers.SerializerMethodField()

    def get_show_time(self, obj):
        return obj.ticket_type.show_time

    class Meta:
        model = Ticket
        # fields = '__all__'
        fields = ('id', 'ticket_type_id', 'number_of_people', 'key', 'total_price', 'show_time', 'buy_time')


class TicketTypeSerializer(serializers.ModelSerializer):
    model = TicketType

    class Meta:
        model = TicketType
        # fields = '__all__'
        fields = ('id', 'name', 'price', 'begin_time', 'end_time', 'number_of_seat', 'remaining_seat', 'image_url', 'content')

