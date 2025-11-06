import re

from django.db import models
from hall.models import Hall

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration of the movie")
    age_rating = models.CharField(max_length=100)
    release_date = models.DateField()
    language = models.CharField(max_length=100)
    trailer_url = models.URLField(blank=True, null=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    @property
    def embed_trailer_url(self):
        """
        Returneaza URL-ul de embed YouTube (https://www.youtube.com/embed/VIDEO_ID)
        pe baza URL-ului standard (watch?v=VIDEO_ID) stocat in baza de date.
        """
        if self.trailer_url and 'watch?v=' in self.trailer_url:
            # Extrage ID-ul video folosind o expresie regulata robusta
            match = re.search(r'(?<=v=)[\w-]+', self.trailer_url)
            if match:
                video_id = match.group(0)
                # Returneaza noul URL in format embed
                return f'https://www.youtube.com/embed/{video_id}'

        # Daca link-ul e deja in format embed, scurt (youtu.be) sau e null, il returneaza asa cum e
        return self.trailer_url

    def __str__(self):
        return self.title

class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie.title} @ {self.start_time.strftime('%Y-%m-%d %H:%M')}"