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
        Extrage ID-ul video din orice format (lung sau scurt) si returneaza
        un URL curat (youtu.be) pentru a asigura parsaarea de catre django-embed-video.
        """
        if self.trailer_url:
            # 1. Incearca sa extraga ID-ul dintr-un URL lung (watch?v=ID...)
            match_v = re.search(r'(?<=v=)[\w-]+', self.trailer_url)

            # 2. Incearca sa extraga ID-ul dintr-un URL scurt (youtu.be/ID...)
            match_short = re.search(r'(?<=youtu\.be/)[\w-]+', self.trailer_url)

            if match_v:
                # Curata ID-ul de parametri suplimentari si returneaza formatul scurt
                video_id = match_v.group(0).split('&')[0]
                return f'https://youtu.be/{video_id}'

            elif match_short:
                # Daca este deja link scurt sau curat, il returneaza
                return self.trailer_url

            # 3. Daca e un link embed (youtube.com/embed/ID), il returneaza
            elif 'youtube.com/embed/' in self.trailer_url:
                return self.trailer_url

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