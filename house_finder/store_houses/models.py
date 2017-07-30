from django.db import models


class House(models.Model):
    site_id = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=100)
    description = models.TextField(default=None)
    price = models.IntegerField()
    url = models.URLField(unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sqft_m2 = models.IntegerField()
    rooms = models.IntegerField()
    baths = models.IntegerField()
    article_update_date = models.CharField(max_length=100)
    is_interesting = models.BooleanField(default=False)
    is_discard = models.BooleanField(default=False)
    has_seen = models.BooleanField(default=False)
    notes = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('site_id', 'website',)
