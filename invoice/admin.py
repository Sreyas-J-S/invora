from django.contrib import admin
from .models import Product, Invoice, InvoiceDetail


# -------------------
# Product Admin
# -------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "cost_price", "selling_price", "product_unit", "product_is_delete")
    search_fields = ("product_name",)
    list_filter = ("product_is_delete",)


# -------------------
# Invoice Detail Inline (for Invoice)
# -------------------
class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 1
    readonly_fields = ("get_total_bill", "get_profit")  # Show auto-calculated values


# -------------------
# Invoice Admin
# -------------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date", "total_sales_amount", "total_profit")
    inlines = [InvoiceDetailInline]
    search_fields = ("customer", "contact", "email")
    list_filter = ("date",)

    def total_sales_amount(self, obj):
        return obj.total_sales_amount
    total_sales_amount.short_description = "Total Sales (₹)"

    def total_profit(self, obj):
        return obj.total_profit
    total_profit.short_description = "Profit (₹)"


# -------------------
# Invoice Detail Admin
# -------------------
@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "amount", "get_total_bill", "get_profit")

    def get_total_bill(self, obj):
        return obj.get_total_bill
    get_total_bill.short_description = "Total (₹)"

    def get_profit(self, obj):
        return obj.get_profit
    get_profit.short_description = "Profit (₹)"
