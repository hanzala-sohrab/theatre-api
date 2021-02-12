from django import forms


class SeatForm(forms.Form):
    occupy_name = forms.CharField(max_length=30, required=False)
    occupy_ticketID = forms.UUIDField(required=False)

    vacate_seat = forms.IntegerField(required=False)

    info_name = forms.CharField(max_length=30, required=False)
    info_ticketID = forms.UUIDField(required=False)
    info_seat = forms.IntegerField(required=False)
