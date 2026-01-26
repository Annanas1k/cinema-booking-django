from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cinemas/', blank=True, null=True)
    description = models.TextField()
    program_phone = models.CharField(max_length=50)
    reservations_phone = models.CharField(max_length=100)
    admin_phone = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100, default="Daily, 10:00 - 23:00")
    google_maps_embed = models.TextField(help_text="Google Maps iframe code")

    @property
    def halls_count(self):
        return self.halls.count()

    def __str__(self):
        return self.name



class News(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    short_description = models.CharField(max_length=250)
    long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AdminTask(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Admin Task"
        verbose_name_plural = "Admin Tasks"
        ordering = ['deadline','-priority']


class ShopCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Shop"

class ShopProducts(models.Model):
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    product_volume = models.PositiveIntegerField(blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='shop_products/', blank=True, null=True)
    product_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name