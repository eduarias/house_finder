from django.db import models


class HousesProvider(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class StartURL(models.Model):
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    provider = models.ForeignKey(HousesProvider)
    url = models.URLField(unique=True)

    def __str__(self):
        return '{0} - {1}'.format(self.provider, self.neighborhood)


class House(models.Model):

    TITLE_MAX_LENGTH = 200

    site_id = models.CharField(max_length=100)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    description = models.TextField(default=None)
    price = models.IntegerField(null=True)
    url = models.URLField(unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    sqft_m2 = models.IntegerField(null=True)
    rooms = models.IntegerField(null=True)
    baths = models.IntegerField(null=True)
    article_update_date = models.CharField(max_length=100)
    is_interesting = models.BooleanField(default=False)
    is_discard = models.BooleanField(default=False)
    has_seen = models.BooleanField(default=False)
    notes = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)
    last_view_at = models.DateTimeField(auto_now=True)
    start_url = models.ForeignKey(StartURL, null=True)

    def __str__(self):
        return self.title

    @property
    def provider(self):
        if self.start_url:
            return self.start_url.provider.name.title()
        else:
            return 'Link'
