from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Invoice, InvoiceDetail
from django.utils import timezone

class BasicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class ProfitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        self.product = Product.objects.create(
            product_name="Test Product",
            cost_price=10.0,
            selling_price=20.0,
            product_unit="Unit"
        )
        
        self.invoice = Invoice.objects.create(
            customer="Test Customer",
            date=timezone.now().date()
        )
        
        # Simulate what the view does: save current prices
        self.detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            product=self.product,
            amount=1,
            cost_price=self.product.cost_price,
            selling_price=self.product.selling_price
        )

    def test_basic_profit_calculation(self):
        """Test that profit is calculated correctly: (20 - 10) * 1 = 10"""
        self.assertEqual(self.invoice.total_profit, 10.0)

    def test_profit_does_not_change_with_product_price(self):
        """Test that profit calculation does NOT change if product price changes (New Behavior)"""
        # Change product selling price
        self.product.selling_price = 30.0
        self.product.save()
        
        # Check if invoice profit remains the same (based on historical price)
        # Expected: (20 - 10) * 1 = 10 (NOT 20)
        self.assertEqual(self.invoice.total_profit, 10.0)
        
    def test_monthly_profit_view(self):
        """Test that the monthly profit view returns correct data"""
        response = self.client.get(reverse('monthly_profit'))
        self.assertEqual(response.status_code, 200)
        # Check if the profit is in the context
        # Note: The view returns JSON strings for months and profits
        self.assertIn('months', response.context)
        self.assertIn('profits', response.context)
