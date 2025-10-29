from django.db import models

class Hall(models.Model):
    name = models.CharFielt(max_length=50)
    total_rows = models.PositiveIntegerField()
    total_columns = models.PositiveIntegerField()

    capacity = models.PositiveIntegerField()
    is_3d = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=11,
                                 choics=[
                                     ('regular', 'Regular'),
                                     ('vip', 'VIP')
                                 ], default='regular')
    is_functional = models.BooleanField(default=False)

    class Meta:
        unique_together = ('hall', 'row', 'column')

    def __str__(self):
        return f"{self.hall.name} - R{self.row}C{self.column}"