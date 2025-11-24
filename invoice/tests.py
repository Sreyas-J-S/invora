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

class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')

    def test_edit_profile_duplicate_username(self):
        """Test that changing username to an existing one handles the error gracefully"""
        self.client.login(username='user1', password='password')
        
        # Try to change user1's username to user2's username
        response = self.client.post(reverse('edit_profile'), {
            'username': 'user2',
            'email': 'user1@example.com'
        })
        
        # Should not crash (500), but return 200 (re-render form) or 302 (redirect)
        # Current broken behavior: crashes with IntegrityError
        self.assertEqual(response.status_code, 302)
        
        # Verify username was NOT changed
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'user1')

    def test_edit_profile_success(self):
        """Test successful profile update"""
        self.client.login(username='user1', password='password')
        
        response = self.client.post(reverse('edit_profile'), {
            'username': 'new_user1',
            'email': 'new_email@example.com'
        })
        
        self.assertEqual(response.status_code, 302) # Redirects on success
        
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'new_user1')
        self.assertEqual(self.user1.email, 'new_email@example.com')

class InvoiceViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.invoice = Invoice.objects.create(
            customer="Test Customer For View",
            date=timezone.now().date(),
            total=100.0
        )

    def test_view_invoice_list(self):
        """Test that the invoice list page shows the created invoice"""
        response = self.client.get(reverse('view_invoice'))
        self.assertEqual(response.status_code, 200)
        
        # Check that the invoice customer name is in the response content
        # This will FAIL if the template loop variable is wrong
        self.assertContains(response, "Test Customer For View")

class InvoiceEditTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.product = Product.objects.create(
            product_name="Test Product",
            cost_price=10.0,
            selling_price=20.0,
            product_unit="Unit"
        )
        
        self.invoice = Invoice.objects.create(
            customer="Original Customer",
            date=timezone.now().date(),
            total=20.0
        )
        
        self.detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            product=self.product,
            amount=1,
            cost_price=10.0,
            selling_price=20.0
        )

    def test_edit_invoice_view_loads(self):
        """Test that the edit invoice page loads"""
        response = self.client.get(reverse('edit_invoice', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Customer")

    def test_edit_invoice_update(self):
        """Test updating an invoice"""
        # Prepare POST data simulating formset
        data = {
            'customer': 'Updated Customer',
            'contact': '1234567890',
            'email': 'updated@example.com',
            'comments': 'Updated comments',
            
            # Management form data
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            
            # Formset data (first row)
            'form-0-product': self.product.pk,
            'form-0-amount': '2', # Changed amount from 1 to 2
        }
        
        response = self.client.post(reverse('edit_invoice', args=[self.invoice.pk]), data)
        
        self.assertEqual(response.status_code, 302) # Redirects to view_invoice
        
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.customer, 'Updated Customer')
        
        # Check details
        details = InvoiceDetail.objects.filter(invoice=self.invoice)
        self.assertEqual(details.count(), 1)
        self.assertEqual(details.first().amount, 2)
        self.assertEqual(self.invoice.total, 40.0) # 2 * 20.0

class InvoicePDFTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.invoice = Invoice.objects.create(
            customer="PDF Customer",
            date=timezone.now().date(),
            total=100.0
        )

    def test_download_invoice_pdf(self):
        """Test that the PDF download view returns a PDF"""
        response = self.client.get(reverse('invoice_pdf', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertIn("filename='Invoice_%s.pdf'" % self.invoice.pk, response['Content-Disposition'])

class InvoicePrintPopupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        self.product = Product.objects.create(
            product_name="Test Product",
            cost_price=10.0,
            selling_price=20.0,
            product_unit="Unit"
        )

    def test_create_invoice_redirects_with_param(self):
        """Test that creating an invoice redirects with new_invoice_id"""
        data = {
            'customer': 'New Customer',
            'contact': '1234567890',
            'email': 'new@example.com',
            'comments': 'New invoice',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-product': self.product.pk,
            'form-0-amount': '1',
        }
        response = self.client.post(reverse('create_invoice'), data)
        
        # Check that it redirects
        self.assertEqual(response.status_code, 302)
        
        # Check that the redirect URL contains the new_invoice_id
        # We need to find the ID of the created invoice
        invoice = Invoice.objects.last()
        expected_url = f"/invoice/view_invoice/?new_invoice_id={invoice.id}"
        # Note: The actual redirect might be relative or absolute, and query params order might vary
        # But here we constructed it simply in the view
        self.assertIn(f"new_invoice_id={invoice.id}", response.url)

    def test_view_invoice_shows_popup_context(self):
        """Test that view_invoice passes new_invoice_id to context"""
        invoice = Invoice.objects.create(
            customer="Popup Customer",
            date=timezone.now().date(),
            total=20.0
        )
        
        response = self.client.get(reverse('view_invoice'), {'new_invoice_id': invoice.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['new_invoice_id']), str(invoice.id))
        self.assertContains(response, 'id="printInvoiceModal"')
        self.assertContains(response, f"/invoice_pdf/{invoice.id}/")
