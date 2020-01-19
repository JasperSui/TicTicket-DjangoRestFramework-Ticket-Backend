from main.models import Ticket, TicketType
from django.db import transaction
import datetime

def UpdateTicketTypeRemainingSeat(ticket_type, number_of_people):

    remaining_seat = ticket_type.remaining_seat

    if remaining_seat >= number_of_people:

        with transaction.atomic():

            ticket_type = TicketType.objects.select_for_update().get(id=ticket_type.id)
            ticket_type.remaining_seat -= number_of_people
            ticket_type.save()

        return True

    else:

        return False