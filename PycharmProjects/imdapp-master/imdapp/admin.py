
# Register your models here.

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Subcategory, Description, Supp,Stock,Supplier,PurchaseBill,PurchaseBillDetails,PurchaseItem,SaleBill,SaleItem,SaleBillDetails

admin.site.register(Stock)
admin.site.register(Supplier)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseBillDetails)
admin.site.register(PurchaseItem)
admin.site.register(SaleBill)
admin.site.register(SaleItem)
admin.site.register(SaleBillDetails)
@admin.register(Category)
class Category(ImportExportModelAdmin):
    pass


@admin.register(Subcategory)
class Subcategory(ImportExportModelAdmin):
    pass


@admin.register(Description)
class Description(ImportExportModelAdmin):
    pass



@admin.register(Supp)
class Supp(ImportExportModelAdmin):
    pass