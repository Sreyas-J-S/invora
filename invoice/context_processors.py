from .models import Product, Invoice, InvoiceDetail
from django.db.models import Sum, F, FloatField

def dashboard_stats(request):
    total_product = Product.objects.count()
    total_invoice = Invoice.objects.count()
    
    # Calculate total income using aggregation for better performance
    total_income_data = InvoiceDetail.objects.aggregate(
        total=Sum(F('selling_price') * F('amount'), output_field=FloatField())
    )
    total_income = total_income_data['total'] or 0
    
    return {
        "total_product": total_product,
        "total_invoice": total_invoice,
        "total_income": total_income,
    }
