from django.db import models, transaction
from content.models import Cinema

class Hall(models.Model):
    name = models.CharField(max_length=50)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, null=True, blank=True, related_name='halls')
    total_rows = models.PositiveIntegerField()
    total_columns = models.PositiveIntegerField()

    capacity = models.PositiveIntegerField()
    is_3d = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.capacity = self.total_rows * self.total_columns

        super().save(*args, **kwargs)

        with transaction.atomic():
            self.seats.filter(row__gt=self.total_rows).delete()
            self.seats.filter(column__gt=self.total_columns).delete()

            existing_seats = set(self.seats.values_list('row', 'column'))
            new_seats = []

            for r in range(1, self.total_rows + 1):
                for c in range(1, self.total_columns + 1):
                    if (r, c) not in existing_seats:
                        new_seats.append(
                            Seat(hall=self, row=r, column=c, is_functional=True)
                        )

            if new_seats:
                Seat.objects.bulk_create(new_seats)



    def __str__(self):
        return f"{self.name} ({self.capacity} seats)"



class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    is_functional = models.BooleanField(default=False)

    class Meta:
        unique_together = ('hall', 'row', 'column')

    def __str__(self):
        return f"{self.hall.name} - R{self.row}C{self.column}"

