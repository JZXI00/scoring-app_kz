from django.contrib import admin
from .models import Client, Report, Blacklist


class ClientAdmin(admin.ModelAdmin):
	list_display = ['name', 'iin', 'age', 'number_credits']
	search_fields = ('name', 'iin')
admin.site.register(Client, ClientAdmin)

class ReportAdmin(admin.ModelAdmin):
	list_display = ['client', 'date_created']
admin.site.register(Report, ReportAdmin)

class BlacklistAdmin(admin.ModelAdmin):
	list_display = ['client', 'date_created', 'is_black']
admin.site.register(Blacklist, BlacklistAdmin)