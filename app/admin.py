from django.contrib import admin
from .models import Topics, Messages, User, Rooms

admin.site.register(User)
admin.site.register(Messages)
admin.site.register(Topics)
admin.site.register(Rooms)

