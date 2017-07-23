from django.db import models


class Home(models.Model):
    site_id = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    url = models.URLField(unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sqft_m2 = models.IntegerField()
    rooms = models.IntegerField()
    baths = models.IntegerField()
    found_on = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    article_update_date = models.CharField(max_length=100)
    is_interesting = models.BooleanField(default=False)
    is_discard = models.BooleanField(default=False)
    has_seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('site_id', 'website',)
