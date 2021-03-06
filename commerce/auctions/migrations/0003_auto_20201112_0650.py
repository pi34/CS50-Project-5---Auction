# Generated by Django 3.1.2 on 2020-11-12 06:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_category_comments_listing_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='interested_buyers',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
