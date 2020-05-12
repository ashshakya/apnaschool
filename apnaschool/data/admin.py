from django.contrib import admin

from apnaschool.data.models import (
    Address, City, State, Department, Standard,
    FeeStructure, StudentsCategory
)

admin.site.register(Address)
admin.site.register(Department)
admin.site.register(Standard)
admin.site.register(FeeStructure)

admin.site.register(StudentsCategory)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_name', 'gst_code')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name', 'state', 'is_active')


# class DocumentAdmin(admin.ModelAdmin):
#     model = Documents
#     list_display = [
#         'document_category', 'doc_type', 'version', 'release_date'
#     ]

#     class Media:
#         js = (
#             '/static/admin/js/assets_admin.js',
#         )
