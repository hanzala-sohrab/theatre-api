from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('seat/occupy/', views.occupy_seat, name='occupy'),
    path('seat/vacate/', views.vacate_seat, name='vacate'),
    path('seat/get_info/<int:seatNo>', views.get_info_by_seat_num, name='info_seat'),
    path('seat/get_info/<uuid:ticketNo>', views.get_info_by_ticket_id, name='info_ticket'),
    path('seat/get_info/<str:pName>', views.get_info_by_name, name='info_name'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
