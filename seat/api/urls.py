from django.urls import path
from seat.api import views

urlpatterns = [
    path('occupy/', views.BookSeat.as_view(), name='occupy'),
    path('vacate/<int:seatNo>', views.VacateSeat.as_view(), name='vacate'),
    path('get_info/<int:seatNo>', views.GetInfoSeatNum.as_view(), name='info_seat'),
    path('get_info/<uuid:ticketNo>', views.GetInfoId.as_view(), name='info_ticket'),
    path('get_info/<str:pName>', views.GetInfoName.as_view(), name='info_name'),
    # path('occupy/', views.occupy_seat, name='occupy'),
    # path('vacate/', views.vacate_seat, name='vacate'),
    # path('get_info/<int:seatNo>', views.get_info_by_seat_num, name='info_seat'),
    # path('get_info/<uuid:ticketNo>', views.get_info_by_ticket_id, name='info_ticket'),
    # path('get_info/<str:pName>', views.get_info_by_name, name='info_name'),
]
