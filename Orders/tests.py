from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from Orders.models import Customer, Product, Order
from unittest.mock import patch
from django.core.mail import send_mail

class CreateOrderTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(username='testuser', email='testuser@example.com', balance=1000)
        self.product = Product.objects.create(name='Test Product', price=200, stock=10)
        self.client.force_authenticate(user=self.customer)

    def test_create_order_success(self):
        """Test successful order creation"""
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(reverse('create_order'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Completed Successfully')

    def test_create_order_insufficient_balance(self):
        """Test order creation with insufficient balance"""
        self.customer.balance = 100  # Less than total price of order
        self.customer.save()
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(reverse('create_order'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insufficient balance')

    def test_create_order_insufficient_stock(self):
        """Test order creation with insufficient stock"""
        data = {
            'product_id': self.product.id,
            'quantity': 20  # More than available stock
        }
        response = self.client.post(reverse('create_order'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stock unavailable')
