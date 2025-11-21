from django import forms
from django.forms import formset_factory
from .models import Product, Invoice, InvoiceDetail


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'cost_price',
            'selling_price',
            'product_unit',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'product_name',
                'placeholder': 'Enter name of the product',
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'cost_price',
                'placeholder': 'Enter cost price of the product',
                'type': 'number',
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'selling_price',
                'placeholder': 'Enter selling price of the product',
                'type': 'number',
            }),
            'product_unit': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'product_unit',
                'placeholder': 'Enter unit of the product',
            }),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'comments',
            'contact',
            'email',
        ]
        widgets = {
            'customer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_customer',
                'placeholder': 'Enter name of the customer',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_contact',
                'placeholder': 'Enter contact of the customer',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'invoice_email',
                'placeholder': 'Enter email of the customer',
            }),
            'comments': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_comments',
                'placeholder': 'Enter comments',
            }),
        }


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
            'product',
            'amount',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_amount',
                'placeholder': '0',
                'type': 'number',
            })
        }


class excelUploadForm(forms.Form):
    file = forms.FileField()


InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)
