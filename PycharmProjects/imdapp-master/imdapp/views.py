

# Create your views here.
import read as read
from django.db.models import Q
from django.http import HttpResponse



import csv

from django.shortcuts import render, redirect, get_object_or_404

from django_filters.views import FilterView
import datetime
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView, TemplateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .filters import StockFilter
from .models import (
    PurchaseBill,
    Supplier,
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,
    SaleItem,
    SaleBillDetails, Stock, Category, Subcategory,
)
from .forms import (
    StockForm,
    SelectSupplierForm,
    PurchaseItemFormset,
    PurchaseDetailsForm,
    SupplierForm,
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm, CategoryForm, SubcategoryForm, DescriptionForm,

)
#
# def addsupplier(request):
#     form=SupplierForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('suppliers-list')
#     context={
#     'form': form
#     }
#     return render(request,"suppliers/edit_supplier.html",context)
#
#
# def supplierlist(request):
#     queryset=Category.objects.all()
#     paginator=Paginator(queryset,10)
#     page_number=request.GET.get('page')
#     queryset=paginator.get_page(page_number)
#     context = {
#         "queryset":queryset
#
#     }
#     return render(request,"/inventory/suppliers",context)


class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/inventory/suppliers'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context

    # used to update a supplier's info


class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/inventory/suppliers'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object': supplier})

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(View):
    def get(self, request,name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': supplierobj,
            'bills': bills
        }
        return render(request, 'suppliers/supplier.html', context)


# shows the list of bills of all purchases
class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10


# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):  # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):  # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class PurchaseCreateView(View):
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)  # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)  # gets the supplier object
        context = {
            'formset': formset,
            'supplier': supplierobj,
        }  # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)  # recieves a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)  # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = PurchaseBill(
                supplier=supplierobj)  # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()  # saves object into the db
            # create bill details object
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:  # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj  # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                # subcategory/stock = get_object_or_404(Stock/Purchase, name=billitem.purchaser/stock.name)       # gets the item

                # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity  # updates quantity
                # purchase/stock.quantity += billitem.quantity                              # updates quantity
                # saves bill item and stock
                stock.save()
                # purchase/stock.save()
                billitem.save()
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset': formset,
            'supplier': supplierobj
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/imdapp/purchases'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            # subcategory/stock = get_object_or_404(/Purchase/Stock, name=item.subcategory/stock.name)
            if stock.is_deleted == False:
                # if subcategory/stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase bill has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)


# stock report

def showresult(request):
    if request.method == "POST":
        fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
        todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
        bills = SaleBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
        return render(request, 'sales/stockreport.html', {"bills": bills})
    else:
        bills = SaleBill.objects.all()
        return render(request, 'sales/stockreport.html', {"bills": bills})

def outwardslip(request):
    if request.method == "POST":
        fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
        todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
        bills = SaleBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
        return render(request, 'sales/outwardslip.html', {"bills": bills})
    else:
        bills = SaleBill.objects.all()
        return render(request, 'sales/outwardslip.html', {"bills": bills})


def inwardslip(request):
    if request.method == "POST":
        fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
        todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
        bills = PurchaseBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
        return render(request, 'purchases/inwardslip.html', {"bills": bills})
    else:
        bills = PurchaseBill.objects.all()
        return render(request, 'purchases/inwardslip.html', {"bills": bills})



# #
# def showresult(request,week,month,year):
#     if request.method == "POST":
#         fromdate = datetime.datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
#         todate = datetime.datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')
#         bills = SaleBill.objects.filter(Q(time__gte=fromdate) & Q(time__lte=todate))
#         return render(request, 'sales/stockreport.html', {"bills": bills})
#     else:
#         bills = SaleBill.objects.all()
#         return render(request, 'sales/stockreport.html', {"bills": bills})


# class StockReportView(ListView):
# model = SaleBill
# template_name = "sales/stockreport.html"
# context_object_name = 'bills'
# ordering = ['time']
# paginate_by = 10

#
# def post(self,request):
#     form = SaleBill(request)
#
#     context = {'form': form}
#     if request.method == "POST":
#         queryset = SaleBill.objects.all()
#         fromdate = request.query_params.get('start_date', None)
#         todate = request.query_params.get('end_date', None)
#         if fromdate and todate:
#             queryset = queryset.filter(date__range=[fromdate, todate])
#             print(queryset)
#         return render(request, "sales/stockreport.html", queryset)
#     return render(request, "sales/stockreport.html", context)
#
#


# shows the list of bills of all sales
class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['time']
    paginate_by = 10


# used to generate a bill object and save items
class SaleCreateView(View):
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)  # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        # purch/stocks = Purchase/Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)  # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.save()
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:  # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj  # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                # stock = get_object_or_404(Stock, name=billitem.stock.name)
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Sold items have been registered successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, self.template_name, context)


class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)


# used to delete a bill object

# used to display the purchase bill object
class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': PurchaseBill.objects.get(billno=billno),
            'items': PurchaseItem.objects.filter(billno=billno),
            'billdetails': PurchaseBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)

            # billdetailsobj.eway = request.POST.get("eway")
            # billdetailsobj.veh = request.POST.get("veh")
            # billdetailsobj.destination = request.POST.get("destination")
            # billdetailsobj.po = request.POST.get("po")
            # billdetailsobj.cgst = request.POST.get("cgst")
            # billdetailsobj.sgst = request.POST.get("sgst")
            # billdetailsobj.igst = request.POST.get("igst")
            # billdetailsobj.cess = request.POST.get("cess")
            # billdetailsobj.tcs = request.POST.get("tcs")
            # billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill': PurchaseBill.objects.get(billno=billno),
            'items': PurchaseItem.objects.filter(billno=billno),
            'billdetails': PurchaseBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }

        return render(request, self.template_name, context)


# used to display the sale bill object
class SaleBillView(View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill': SaleBill.objects.get(billno=billno),
            'items': SaleItem.objects.filter(billno=billno),
            'billdetails': SaleBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill': SaleBill.objects.get(billno=billno),
            'items': SaleItem.objects.filter(billno=billno),
            'billdetails': SaleBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                      str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Billno', 'Customer', 'Stock Sold', 'Quatity Sold', 'Total Sold Price', 'Date'])

    expenses = SaleItem.objects.all()

    for x in expenses:
        writer.writerow([x.billno.billno, x.billno.name, x.stock, x.quantity, x.totalprice, x.billno.time])
    return response


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory/inventory.html'
    paginate_by = 10



class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "inventory/edit_stock.html"
    success_url = '/inventory'
    success_message = "Stock has been created successfully"

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'

        return context


class StockUpdateView(SuccessMessageMixin, UpdateView):  # updateview class to edit stock, mixin used to display message
    model = Stock  # setting 'Stock' model as model
    form_class = StockForm  # setting 'StockForm' form as form
    template_name = "inventory/edit_stock.html"  # 'edit_stock.html' used as the template
    success_url = '/inventory'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'

        return context


class StockDeleteView(View):  # view class to delete stock
    template_name = "inventory/delete_stock.html"  # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"  # displays message when form is submitted

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object': stock})

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('inventory')


class StockView(View):
    def get(self, request, name):
        stockobj = get_object_or_404(Stock, name=name)
        # stock = Stock.objects.get(stock=stockobj)

        context = {
            'stock': stockobj,
        }
        return render(request, 'inventory/stockdetails.html', context)




def addcategory(request):
    form=CategoryForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
            # return redirect('inventory')
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/addcat.html", locals())

def addsubcategory(request):
    form=SubcategoryForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
            # return redirect('inventory')
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request,"Master/addsubcategory.html",locals())


def adddescription(request):
    form=DescriptionForm(request.POST or None)
    try:
        error = "no"
        if form.is_valid():
            form.save()
            # return redirect('inventory')
        else:
            error = "yes"
    except:
        error = "yes"
    return render(request, "Master/adddescription.html", locals())
#
# def add(request):
#     form=CategoryForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('category-list')
#     context={
#     'form': form
#     }
#     return render(request,"Master/addcategory.html",context)


# def categorylist(request):
#     queryset=Category.objects.all()
#     paginator=Paginator(queryset,10)
#     page_number=request.GET.get('page')
#     queryset=paginator.get_page(page_number)
#     context = {
#         "queryset":queryset
#
#     }
#     return render(request,"Master/category_list.html",context)


def delete_category(request ,id):
    print(id)
    Category.objects.get(id = id).delete()
    return redirect('category-list')



class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = '/inventory/Master'
    success_message = "Category details has been updated successfully"
    template_name = "Master/update_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'

        return context














#
# def update_category(request, pk):
#     category = Category.objects.get(pk = pk)
#     category.category = category
#     category.save()
#     #return render(request, 'index.html')
#     return redirect('category-list')

# class CategoryListView(ListView):
#     model = Category
#     template_name = 'Master/category_list.html'
#     queryset = Category.objects.filter(is_deleted=False)
#     paginate_by = 10
#     paginator = Paginator(keywords, per_page=2)
#
#
# class CategoryCreateView(SuccessMessageMixin, CreateView):
#     model = Category
#     form_class = CategoryForm
#     success_url = '/inventory/Master'
#     success_message = "Category has been created successfully"
#     template_name = "Master/addcategory.html"
#
#     def get_context_data(self, **kwargs):  # used to send additional context
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'New Category'
#         context["savebtn"] = 'Add Category'
#         return context




