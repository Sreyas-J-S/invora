from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from utils.filehandler import handle_file_upload
from .forms import *
from .models import *
from .models import *
import pandas as pd
from django.db.models import Sum, F, FloatField
from django.db.models.functions import TruncMonth
import json


# -------------------
# Utility
# -------------------
def getTotalIncome():
    """Total of all invoices (sales, not profit)."""
    allInvoice = Invoice.objects.all()
    totalIncome = sum(invoice.total_sales_amount for invoice in allInvoice)
    return totalIncome


# -------------------
# Dashboard
# -------------------
@login_required
def base(request):
    total_product = Product.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()
    context = {
        "total_product": total_product,
        "total_invoice": total_invoice,
        "total_income": total_income,
    }
    return render(request, "invoice/base/base.html", context)


# -------------------
# Create Product
# -------------------
@login_required
def create_product(request):
    product = ProductForm()
    if request.method == "POST":
        product = ProductForm(request.POST)
        if product.is_valid():
            product.save()
            messages.success(request, "Product created successfully!")
            return redirect("view_product")

    context = {
        "product": product,
    }
    return render(request, "invoice/create_product.html", context)


@login_required
def view_product(request):
    product = Product.objects.filter(product_is_delete=False)
    context = {
        "product": product,
    }
    return render(request, "invoice/view_product.html", context)


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("view_product")

    context = {
        "product": form,
    }
    return render(request, "invoice/create_product.html", context)


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.product_is_delete = True
    product.save()
    messages.success(request, "Product deleted successfully!")
    return redirect("view_product")


# -------------------
# Create Invoice
# -------------------
@login_required
def create_invoice(request):
    form = InvoiceForm()
    formset = InvoiceDetailFormSet()

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.save()

            total = 0
            for f in formset:
                if f.cleaned_data:
                    product = f.cleaned_data.get("product")
                    amount = f.cleaned_data.get("amount")
                    if product and amount:
                        detail = InvoiceDetail(
                            invoice=invoice,
                            product=product,
                            amount=amount,
                            cost_price=product.cost_price,
                            selling_price=product.selling_price
                        )
                        detail.save()
                        total += detail.get_total_bill

            invoice.total = total
            invoice.save()
            messages.success(request, "Invoice created successfully!")
            invoice.total = total
            invoice.save()
            messages.success(request, "Invoice created successfully!")
            return redirect(f"{reverse('view_invoice')}?new_invoice_id={invoice.id}")

    context = {
        "form": form,
        "formset": formset,
    }
    return render(request, "invoice/create_invoice.html", context)


@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    form = InvoiceForm(instance=invoice)
    
    # Prepare initial data for formset
    invoice_details = InvoiceDetail.objects.filter(invoice=invoice)
    initial_data = []
    for detail in invoice_details:
        initial_data.append({
            'product': detail.product,
            'amount': detail.amount,
        })
    
    formset = InvoiceDetailFormSet(initial=initial_data)
    # We need to ensure the formset has enough forms for existing data
    # formset.extra = 0 # Optional: don't show extra empty rows if we have data? 
    # Actually, formset_factory with initial data will create forms for initial data + extra.
    # But we want to populate them.
    
    # Better approach for formset with initial data:
    # The formset_factory doesn't automatically bind model instances like inlineformset_factory.
    # Since we are using a standard formset, we pass 'initial' list.
    
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDetailFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.save()

            # Delete existing details to replace with new ones
            # This is a simple strategy for "editing" - replace all items
            InvoiceDetail.objects.filter(invoice=invoice).delete()

            total = 0
            for f in formset:
                if f.cleaned_data:
                    product = f.cleaned_data.get("product")
                    amount = f.cleaned_data.get("amount")
                    if product and amount:
                        detail = InvoiceDetail(
                            invoice=invoice,
                            product=product,
                            amount=amount,
                            cost_price=product.cost_price,
                            selling_price=product.selling_price
                        )
                        detail.save()
                        total += detail.get_total_bill

            invoice.total = total
            invoice.save()
            messages.success(request, "Invoice updated successfully!")
            return redirect("view_invoice")

    context = {
        "form": form,
        "formset": formset,
    }
    return render(request, "invoice/create_invoice.html", context)


@login_required
def view_invoice(request):
    invoices = Invoice.objects.all().order_by('-id')
    
    new_invoice_id = request.GET.get('new_invoice_id')
    
    context = {
        "invoices": invoices,
        "new_invoice_id": new_invoice_id,
    }
    return render(request, "invoice/view_invoice.html", context)


@login_required
def view_invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    context = {
        "invoice": invoice,
        "invoice_detail": invoice_detail,
        "total_sales": invoice.total_sales_amount,
        "total_profit": invoice.total_profit,
    }
    return render(request, "invoice/view_invoice_detail.html", context)


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")

    context = {
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }
    context = {
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }
    return render(request, "invoice/delete_invoice.html", context)


@login_required
def monthly_profit(request):
    monthly_stats = InvoiceDetail.objects.filter(
        invoice__isnull=False,
        product__isnull=False
    ).annotate(
        month=TruncMonth('invoice__date')
    ).values('month').annotate(
        profit=Sum(
            (F('selling_price') - F('cost_price')) * F('amount'),
            output_field=FloatField()
        )
    ).order_by('month')

    months = []
    profits = []
    for stat in monthly_stats:
        if stat['month']:
            months.append(stat['month'].strftime('%B %Y'))
            profits.append(stat['profit'])

    context = {
        'months': json.dumps(months),
        'profits': json.dumps(profits),
    }
    context = {
        'months': json.dumps(months),
        'profits': json.dumps(profits),
    }
    return render(request, 'invoice/monthly_profit.html', context)


@login_required
def download_all(request):
    # Get all invoices
    invoices = Invoice.objects.all()

    # Create a list of dictionaries
    data = []
    for invoice in invoices:
        data.append({
            'Date': invoice.date,
            'Customer': invoice.customer,
            'Contact': invoice.contact,
            'Email': invoice.email,
            'Comments': invoice.comments,
            'Total': invoice.total,
            'Profit': invoice.total_profit,
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create response
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="invoices.xlsx"'

    # Write to response
    df.to_excel(response, index=False)

    return response


@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        user = request.user
        
        # Check if username already exists for a different user
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already taken. Please choose another one.')
            return redirect('edit_profile')

        user.username = username
        user.email = email
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('edit_profile')
        
    return render(request, 'invoice/edit_profile.html')


@login_required
def download_invoice_pdf(request, pk):
    from .utils import generate_invoice_pdf
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    
    pdf_content = generate_invoice_pdf(invoice, invoice_detail)
    
    response = HttpResponse(bytes(pdf_content), content_type='application/pdf')
    filename = "Invoice_%s.pdf" % (invoice.id)
    content = "inline; filename='%s'" % (filename)
    response['Content-Disposition'] = content
    return response
