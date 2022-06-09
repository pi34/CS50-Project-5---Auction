from django.contrib import admin
from auctions.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)