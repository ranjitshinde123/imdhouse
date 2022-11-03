from django.db import models

# Create your models here.



class Category(models.Model):
    id=models.IntegerField(primary_key=True)
    category=models.CharField(max_length=255)
    subcategory=models.CharField(max_length=255)
    description=models.TextField(max_length=255)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.category

    class Meta:
        db_table='Category'

class Subcategory(models.Model):
    id=models.IntegerField(primary_key=True)
    subcategory=models.CharField(max_length=255)
    is_consumable=models.BooleanField(default=False)
    def __str__(self):
        return self.subcategory
    class Meta:
        db_table='Subcategory'


class Description(models.Model):
    id=models.IntegerField(primary_key=True)

    description=models.CharField(max_length=255)
    def __str__(self):
        return self.description

    class Meta:
        db_table='Description'

class Supp(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)


    def __str__(self):
        return self.name
    class Meta:
        db_table='Supp'




class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Supp,on_delete=models.CharField)
    phone = models.CharField(max_length=12, unique=True)
    address = models.TextField()
    email = models.EmailField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class Stock(models.Model):
    STATUS_CHOICE = [
        ('CONSUMABLE', 'CONSUMABLE'),
        ('NON-COMSUMABLE', 'NON-COMSUMABLE'),
    ]
    STATUS_UNIT = [
        ('Mtr', 'Mtr'),
        ('Cm', 'Cm'),
        ('mm', 'mm'),
        ('Kg', 'Kg'),
        ('gm', 'gm'),
        ('Ltr', 'Ltr'),
        ('SqMtr', 'SqMtr'),
        ('SqCm', 'SqCm'),
        ('CuM', 'CuM'),
        ('Ream', 'Ream'),
        ('Doz', 'Doz'),
        ('Pkts', 'Pkts'),
        ('Pairs', 'Pairs'),
        ('Rolls', 'Rolls'),
        ]

    CONDITION = [
        ('GOOD', 'GOOD'),
        ('TORED', 'TORED'),
        ('DAMAGED', 'DAMAGED'),
    ]
    MODE_OF_DELEVERY = [
        ('BY-HAND', 'BY-HAND'),
        ('COURIER', 'COURIER'),
        ('OTHER', 'OTHER'),

    ]
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    description=models.ForeignKey(Description,on_delete=models.CASCADE)
    name=models.ForeignKey(Supp,on_delete=models.CASCADE)
    type=models.CharField(max_length=50, choices=STATUS_CHOICE)
    unit=models.CharField(max_length=50,choices=STATUS_UNIT)
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=1)
    Mode_of_delivery = models.CharField(max_length=50, choices=MODE_OF_DELEVERY)  # received by
    label_code = models.CharField(max_length=20, default="")
    condition = models.CharField(max_length=50, choices=CONDITION)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subcategory)






class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchasesupplier')

    def __str__(self):
        return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total



class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasedetailsbillno')
    total = models.CharField(max_length=50, blank=True, null=True)
    is_deleted=models.BooleanField(default=False)


    def __str__(self):
        return "Bill no: " + str(self.billno.billno)

class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.subcategory




class SaleBill(models.Model):

    CONDITION = [
        ('GOOD', 'GOOD'),
        ('TORED', 'TORED'),
        ('DAMAGED', 'DAMAGED'),
    ]
    MODE_OF_DELEVERY = [
        ('BYHAND', 'BYHAND'),
        ('COURIOR', 'COURIOR'),
        ('OTHER', 'OTHER'),

    ]

    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    Mode_of_delivery = models.CharField(max_length=50, choices=MODE_OF_DELEVERY)  # received by
    label_code = models.CharField(max_length=20, default="")
    issued_to = models.CharField(max_length=50)
    # condition = models.CharField(max_length=50, choices=CONDITION)
    is_deleted=models.BooleanField(default=False)




    def __str__(self):
        return str(self.name)



    def __str__(self):
        return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)

    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total


# contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    # def __str__(self):
    #     return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name
    def __str__(self):
        return "Bill no: " + str(self.billno.billno)

        # return  "Bill no: " + str(self.billno.billno),"Stock Name: " + str(self.stock.subcategory)




# contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='saledetailsbillno')

    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Bill no: " + (self.billno.billno)



