from django.db import models
from django.utils import timezone


# -------------------
# Product Model
# -------------------
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    cost_price = models.FloatField(default=0)  # New field: Cost of the product
    selling_price = models.FloatField(default=0)  # New field: Selling price
    product_unit = models.CharField(max_length=255)
    product_is_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product_name)


# -------------------
# Invoice Model
# -------------------
class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    customer = models.TextField(default='')
    contact = models.CharField(max_length=255, default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)
    comments = models.TextField(default='', blank=True, null=True)
    total = models.FloatField(default=0)  # Will be auto-calculated

    def __str__(self):
        return f"Invoice {self.id} - {self.customer}"

    @property
    def total_profit(self):
        """Sum of profit from all items in this invoice"""
        details = self.invoicedetail_set.all()
        return sum([detail.get_profit for detail in details])

    @property
    def total_sales_amount(self):
        """Total sales amount of this invoice"""
        details = self.invoicedetail_set.all()
        return sum([detail.get_total_bill for detail in details])


# -------------------
# Invoice Detail Model
# -------------------
class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=1)
    cost_price = models.FloatField(default=0)  # Stored at time of sale
    selling_price = models.FloatField(default=0)  # Stored at time of sale

    @property
    def get_total_bill(self):
        """Total sale amount for this product in the invoice"""
        if self.selling_price:
            return float(self.selling_price) * float(self.amount)
        return 0

    @property
    def get_profit(self):
        """Profit for this product in the invoice"""
        if self.selling_price:
            return (float(self.selling_price) - float(self.cost_price)) * float(self.amount)
        return 0
