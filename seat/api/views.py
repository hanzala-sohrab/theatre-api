from seat.models import Seat
from rest_framework.decorators import api_view
from .serializers import SeatSerializer
from rest_framework.response import Response
from rest_framework import status
from theatre.settings import MAX_OCCUPANCY
from queue import Queue
from rest_framework import generics


# Overriding Django's default 404 with custom JSON response
@api_view(['GET'])
def error_404(request):
    return Response(status=status.HTTP_404_NOT_FOUND)


# Occupy seat
class BookSeat(generics.CreateAPIView):
    model = Seat
    serializer_class = SeatSerializer

    vacantSeats = Queue(maxsize=MAX_OCCUPANCY)

    def perform_create(self, serializer):
        serializer.save(seatNum=self.vacantSeats.get(), status=True)

    def create(self, request, *args, **kwargs):
        self.vacantSeats = Queue(maxsize=MAX_OCCUPANCY)
        for i in range(1, MAX_OCCUPANCY + 1):
            try:
                seat = Seat.objects.get(seatNum=i)
            except Seat.DoesNotExist:
                self.vacantSeats.put(i)

        if self.vacantSeats.empty():
            return Response(
                {"message": "Show is houseful. No more bookings can be made!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Vacate seat
class VacateSeat(generics.DestroyAPIView):
    model = Seat
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()

    def delete(self, request, *args, **kwargs):
        print(kwargs)
        seatNo = kwargs['seatNo']
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


# Get person/seat information by seat number
class GetInfoSeatNum(generics.ListAPIView):
    model = Seat
    serializer_class = SeatSerializer

    def get_queryset(self):
        return self.model.objects.filter(seatNum=self.kwargs['seatNo'])


# Get person/seat information by ticket ID
class GetInfoId(generics.ListAPIView):
    model = Seat
    serializer_class = SeatSerializer

    def get_queryset(self):
        return self.model.objects.filter(ticketID=self.kwargs['ticketNo'])


# Get person/seat information by person's name
class GetInfoName(generics.ListAPIView):
    model = Seat
    serializer_class = SeatSerializer

    def get_queryset(self):
        return self.model.objects.filter(name=self.kwargs['pName'])

# # Occupy seat
# @api_view(['POST'])
# def occupy_seat(request):
#     """
#     :param request: A Request object containing a person's name and a ticket ID.
#     :return: A Response object denoting the allocated seat number.
#
#     API endpoint for booking a seat.
#
#     If the seating is full, the appropriate error message is returned
#     """
#     print(request)
#     vacantSeats = Queue(maxsize=MAX_OCCUPANCY)
#     for i in range(1, MAX_OCCUPANCY + 1):
#         try:
#             seat = Seat.objects.get(seatNum=i)
#         except Seat.DoesNotExist:
#             vacantSeats.put(i)
#     if vacantSeats.empty():
#         return Response(
#             {
#                 "message": "Show is houseful. No more bookings can be made!"
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     else:
#         request.data['seatNum'] = vacantSeats.get()
#         request.data['status'] = True
#         serializer = SeatSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Vacate seat
# @api_view(['DELETE'])
# def vacate_seat(request):
#     """
#     :param request: A Request object containing a seat number.
#     :return: A Response object denoting the vacation of a seat if it was already occupied.
#
#     API endpoint for deallocating a seat.
#     """
#     print(request.data.keys())
#     seatNo = request.data['seatNum']
#     context = {}
#     try:
#         seat = Seat.objects.get(seatNum=seatNo)
#         seat.delete()
#         context["message"] = f"Seat number {seatNo} is now vacant!"
#         _status = status.HTTP_200_OK
#     except Seat.DoesNotExist:
#         context["message"] = f"Seat number {seatNo} is already vacant. Please provide another seat number!"
#         _status = status.HTTP_400_BAD_REQUEST
#     return Response(context, status=_status)
#
#
# @api_view(['GET'])
# def get_info_by_seat_num(request, seatNo):
#     """
#     :param request: A Request object
#     :param seatNo: A seat number
#     :return: A Response object containing the person's name, ticket ID, and seat number.
#
#
#     API endpoint for getting a person's info by his/her seat number
#     """
#     try:
#         seat = Seat.objects.get(seatNum=seatNo)
#         serializer = SeatSerializer(seat)
#         return Response(serializer.data)
#     except Seat.DoesNotExist:
#         return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
#
#
# @api_view(['GET'])
# def get_info_by_ticket_id(request, ticketNo):
#     """
#     :param request: A Request object
#     :param ticketNo: A ticket ID
#     :return: A Response object containing the person's name, ticket ID, and seat number.
#
#     API endpoint for getting a person's info by his/her ticket ID
#     """
#     try:
#         seat = Seat.objects.get(ticketID=ticketNo)
#         serializer = SeatSerializer(seat)
#         return Response(serializer.data)
#     except Seat.DoesNotExist:
#         return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
#
#
# @api_view(['GET'])
# def get_info_by_name(request, pName):
#     """
#     :param request: A Request object
#     :param pName: A person's name
#     :return: A Response object containing the person's name, ticket ID, and seat number.
#
#     API endpoint for getting a person's info by his/her name
#     """
#     try:
#         seats = Seat.objects.filter(name=pName)
#         seat = seats[0]
#         serializer = SeatSerializer(seats, many=True)
#         return Response(serializer.data)
#     except Seat.DoesNotExist:
#         return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
#     except IndexError:
#         return Response({"message": "No information found!"}, status=status.HTTP_404_NOT_FOUND)
