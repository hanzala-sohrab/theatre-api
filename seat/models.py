from django.db import models


class Seat(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Person's name", max_length=30)
    seatNum = models.IntegerField(primary_key=True, verbose_name="Seat number", unique=True)
    ticketID = models.UUIDField(
        verbose_name="Ticket ID",
        unique=True
    )
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
