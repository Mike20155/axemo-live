from django.contrib import admin
from .models import DebitTransaction, Address, History

# Register your models here.

admin.site.register(DebitTransaction)
admin.site.register(History)
admin.site.register(Address)


