from rest_framework.decorators import api_view
from .models import Seat
from .serializers import SeatSerializer
from django.shortcuts import redirect
from .forms import SeatForm
from django.views.generic.edit import FormView
from rest_framework.response import Response
from rest_framework import status
from theatre.settings import MAX_OCCUPANCY
from queue import Queue


# class Index(FormView):
#     template_name = 'seat/index.html'
#     form_class = SeatForm
#
#     def form_valid(self, form):
#         print(self.request.POST)
#         # occupy_name = form.cleaned_data.get('occupy_name')
#         # occupy_ticketID = form.cleaned_data.get('occupy_ticketID')
#         #
#         # vacate_seat = form.cleaned_data.get('vacate_seat')
#         #
#         # info_name = form.cleaned_data.get('info_name')
#         # info_ticketID = form.cleaned_data.get('info_ticketID')
#         # info_seat = form.cleaned_data.get('info_seat')
#         #
#         # if occupy_name != '' and occupy_ticketID != '':
#         if 'occupy' in self.request.POST:
#             return redirect('occupy', self.request)
#         # elif vacate_seat != '':
#         #     if 'vacate' in self.request.POST:
#         #         return redirect('vacate', vacate_seat)
#         # else:
#         #     return redirect('branches', info_name, info_ticketID, info_seat)


# Overriding Django's default 404 with custom JSON response
@api_view(['GET'])
def error_404(request):
    return Response(status=status.HTTP_404_NOT_FOUND)


# Occupy seat
@api_view(['POST'])
def occupy_seat(request):
    """
    :param request: A Request object containing a person's name and a ticket ID.
    :return: A Response object denoting the allocated seat number.

    API endpoint for booking a seat.

    If the seating is full, the appropriate error message is returned
    """
    print(type(request))
    vacantSeats = Queue(maxsize=MAX_OCCUPANCY)
    for i in range(1, MAX_OCCUPANCY + 1):
        try:
            seat = Seat.objects.get(seatNum=i)
        except Seat.DoesNotExist:
            vacantSeats.put(i)
    if vacantSeats.empty():
        return Response(
            {
                "message": "Show is houseful. No more bookings can be made!"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        request.data['seatNum'] = vacantSeats.get()
        request.data['status'] = True
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vacate seat
@api_view(['DELETE'])
def vacate_seat(request):
    """
    :param request: A Request object containing a seat number.
    :return: A Response object denoting the vacation of a seat if it was already occupied.

    API endpoint for deallocating a seat.
    """
    seatNo = request.data['seatNum']
    context = {}
    try:
        seat = Seat.objects.get(seatNum=seatNo)
        seat.delete()
        context["message"] = f"Seat number {seatNo} is now vacant!"
        _status = status.HTTP_200_OK
    except Seat.DoesNotExist:
        context["message"] = f"Seat number {seatNo} is already vacant. Please provide another seat number!"
        _status = status.HTTP_400_BAD_REQUEST
    return Response(context, status=_status)


@api_view(['GET'])
def get_info_by_seat_num(request, seatNo):
    """
    :param request: A Request object
    :param seatNo: A seat number
    :return: A Response object containing the person's name, ticket ID, and seat number.

    API endpoint for getting a person's info by his/her seat number
    """
    try:
        seat = Seat.objects.get(seatNum=seatNo)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)
    except Seat.DoesNotExist:
        return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_info_by_ticket_id(request, ticketNo):
    """
    :param request: A Request object
    :param ticketNo: A ticket ID
    :return: A Response object containing the person's name, ticket ID, and seat number.

    API endpoint for getting a person's info by his/her ticket ID
    """
    try:
        seat = Seat.objects.get(ticketID=ticketNo)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)
    except Seat.DoesNotExist:
        return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_info_by_name(request, pName):
    """
    :param request: A Request object
    :param pName: A person's name
    :return: A Response object containing the person's name, ticket ID, and seat number.

    API endpoint for getting a person's info by his/her name
    """
    try:
        seats = Seat.objects.filter(name=pName)
        seat = seats[0]
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
    except Seat.DoesNotExist:
        return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
