from django.contrib import admin
from .models import Tickets, Contacts, Inquiry

# Register your models here.

admin.site.register(Tickets)
admin.site.register(Contacts)
admin.site.register(Inquiry)


