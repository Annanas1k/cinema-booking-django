import re

from django.db import models
from hall.models import Hall
from embed_video.fields import EmbedVideoField # <-- Import NOU

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration of the movie")
    age_rating = models.CharField(max_length=100)
    release_date = models.DateField()
    language = models.CharField(max_length=100)
    trailer_url = EmbedVideoField(blank=True, null=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    @property
    def clean_trailer_link(self):
        """
        Returneaza linkul YouTube in format embed (https://www.youtube.com/embed/VIDEO_ID),
        indiferent de formatul initial (watch, youtu.be, embed etc.).
        """

        if not self.trailer_url:
            return None

        url = self.trailer_url.strip()

        # Extrage ID-ul din toate formatele posibile
        patterns = [
            r'(?:v=|\/embed\/|youtu\.be\/)([A-Za-z0-9_-]{11})',  # ID din watch?v=, /embed/, youtu.be/
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube-nocookie.com/embed/{video_id}'

        # Daca nu gaseste niciun ID valid
        return None
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