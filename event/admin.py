from django.contrib import admin
from .models import Event, Registration, Invitation
# Register your models here.
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Invitation)