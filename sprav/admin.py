from django.contrib import admin
from django.contrib.auth.models import Permission
from sprav.models import *


class SimpleSpravAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']

class PolymersAdmin(admin.ModelAdmin):
    change_list_template = "admin/sprav/Polymers/change_list.html"
    list_display = ('shortcode', )
    list_filter = ('subtype__type__name', 'subtype__name', 'plants__name')
    ordering = ['shortcode']

# Register your models here.
admin.site.register(Applications, SimpleSpravAdmin)
admin.site.register(ApplicationCategorys, SimpleSpravAdmin)
admin.site.register(Colors, SimpleSpravAdmin)
admin.site.register(Modifications, SimpleSpravAdmin)
admin.site.register(Copolymers, SimpleSpravAdmin)
admin.site.register(ObtainingMethods, SimpleSpravAdmin)
admin.site.register(ProcessingMethods, SimpleSpravAdmin)
admin.site.register(Types, SimpleSpravAdmin)
admin.site.register(Subtypes, SimpleSpravAdmin)
admin.site.register(Plants, SimpleSpravAdmin)
admin.site.register(Polymers, PolymersAdmin)
admin.site.register(Permission)