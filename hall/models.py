from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=50)
    total_rows = models.PositiveIntegerField()
    total_columns = models.PositiveIntegerField()

    capacity = models.PositiveIntegerField()
    is_3d = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     # Asigură-te că capacitatea este calculată corect
    #     self.capacity = self.total_rows * self.total_columns
    #     is_new = self.pk is None  # Verifică dacă este o sală nouă
    #     super().save(*args, **kwargs)
    #
    #     # Generează locurile DOAR dacă sala este nouă și nu are locuri deja
    #     if is_new:  # Generăm locurile o singură dată la creare
    #         self.generate_seats()
    #
    # def generate_seats(self):
    #     """Creează automat toate locurile (Seat) pentru această sală."""
    #     # Se asigură că șterge orice locuri vechi înainte de regenerare (opțional)
    #     self.seats.all().delete()
    #
    #     seats_to_create = []
    #     for row in range(1, self.total_rows + 1):
    #         for column in range(1, self.total_columns + 1):
    #             # Setează locurile VIP (de exemplu, primele 2 rânduri)
    #             seat_type = 'vip' if row <= 2 and self.is_vip else 'regular'
    #
    #             seats_to_create.append(
    #                 Seat(
    #                     hall=self,
    #                     row=row,
    #                     column=column,
    #                     seat_type=seat_type,
    #                     is_functional=True
    #                 )
    #             )
    #     # Inserare în masă pentru performanță
    #     Seat.objects.bulk_create(seats_to_create)


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=11,
                                 choices=[
                                     ('regular', 'Regular'),
                                     ('vip', 'VIP')
                                 ], default='regular')
    is_functional = models.BooleanField(default=False)

    class Meta:
        unique_together = ('hall', 'row', 'column')

    def __str__(self):
        return f"{self.hall.name} - R{self.row}C{self.column}"

