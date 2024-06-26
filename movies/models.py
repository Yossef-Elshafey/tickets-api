from django.db import models
from django.utils.text import slugify


class Movie(models.Model):
    class Meta:
        db_table = "Movie"

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/movies/")
    release_date = models.DateField()
    duration = models.DecimalField(max_digits=3, decimal_places=2)
    avaliable = models.BooleanField(default=True)
    slug = models.SlugField(default="", null=True, blank=True)
    hall_id = models.ForeignKey("hall.Hall", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
