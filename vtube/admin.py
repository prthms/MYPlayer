from django.contrib import admin
from .models import Channels, Videos, userHistory
# Register your models here.
admin.site.register(Channels)
admin.site.register(Videos)
admin.site.register(userHistory)