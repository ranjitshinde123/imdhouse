from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static



urlpatterns = [


    path('', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
    path('stock/<name>', views.StockView.as_view(), name='stockdetails'),
    path('stock/<name>', views.StockView.as_view(), name='stockdetails'),


    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'),
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'),
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

    path('sales/', views.SaleView.as_view(), name='sales-list'),
    # path('stockreport/', views.showresult, name='stockreport'),
    path('outwardslip/', views.outwardslip, name='outwardslip'),
    path('inwardslip/', views.inwardslip, name='inwardslip'),

    path('export/', views.export_csv, name='stockre'),
    # path('filterrange/', views.showresult,name='stockreport'),

    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),

    # path('Master/', views.categorylist, name='category-list'),
    path('Master/new',views.addcategory, name='addcategory'),
    path('Master/subcategory',views.addsubcategory, name='addsubcategory'),
    path('Master/description',views.adddescription, name='adddescription'),



    path('Master/<pk>/edit', views.CategoryUpdateView.as_view(), name='update-category'),
    path('Master/deleteproduct/<int:id>', views.delete_category, name='delete-category'),
    # path('Master/updatecategory/<pk>/edit', views.update_category, name='update-category'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

