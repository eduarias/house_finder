from django.db import models


class HousesProvider(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=150)
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=150)
    district = models.ForeignKey(District, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StartURL(models.Model):
    TYPE = (('R', 'Rent'),
            ('B', 'Buy'))
    city = models.ForeignKey(City, null=False, on_delete=models.PROTECT)
    district = models.ForeignKey(District, null=True, on_delete=models.SET_NULL)
    neighborhood = models.ForeignKey(Neighborhood, null=True, on_delete=models.SET_NULL)
    provider = models.ForeignKey(HousesProvider)
    type = models.CharField(max_length=1, choices=TYPE, default='R')
    url = models.URLField(unique=True)

    def __str__(self):
        return '{0} - {1} - {2} - {3}'.format(self.provider, self.city, self.district, self.neighborhood)


class House(models.Model):

    TITLE_MAX_LENGTH = 500

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
    start_url = models.ForeignKey(StartURL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    @property
    def provider(self):
        if self.start_url:
            return self.start_url.provider.name.title()
        else:
            return 'Link'
