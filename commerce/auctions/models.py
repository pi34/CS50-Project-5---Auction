from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.CharField(max_length=2000, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    interested_buyers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Bids(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid} by {self.user} on {self.listing}"

class Comments(models.Model):
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

