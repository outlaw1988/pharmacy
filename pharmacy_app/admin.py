from django.contrib import admin
from .models import Medicine, MedicineCategory, MedicineUnit, MedicineSale


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'producer', 'url', 'count', 'date_added', 'price')


@admin.register(MedicineUnit)
class MedicineUnitAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'status', 'date_added', 'date_updated')


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(MedicineSale)
class MedicineSaleAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'items_count', 'amount', 'purchase_date']
