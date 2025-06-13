import requests
import json
import unittest
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load environment variables from frontend .env file to get the backend URL
frontend_env_path = Path('/app/frontend/.env')
load_dotenv(frontend_env_path)

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Append /api to the backend URL
API_URL = f"{BACKEND_URL}/api"
print(f"Testing API at: {API_URL}")

class TestShriyanshRestaurantAPI(unittest.TestCase):
    
    def test_01_root_endpoint(self):
        """Test the root endpoint"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Welcome to Shriyansh Restaurant API")
        print("✅ Root endpoint test passed")
    
    def test_02_restaurant_info(self):
        """Test the restaurant info endpoint"""
        response = requests.get(f"{API_URL}/restaurant-info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Shriyansh Restaurant")
        self.assertEqual(data["address"], "Narsinghpur, Madhya Pradesh, India")
        self.assertIn("Pure Vegetarian", data["specialties"])
        self.assertIn("Takeout", data["services"])
        self.assertIn("Delivery", data["services"])
        self.assertIn("Catering", data["services"])
        print("✅ Restaurant info endpoint test passed")
    
    def test_03_create_menu_item(self):
        """Test creating a new menu item"""
        test_item = {
            "name": "Paneer Tikka",
            "description": "Marinated cottage cheese cubes grilled to perfection",
            "price": 250.0,
            "category": "appetizers",
            "is_spicy": True,
            "preparation_time": 20,
            "ingredients": ["Paneer", "Yogurt", "Spices", "Bell Peppers", "Onions"]
        }
        
        response = requests.post(f"{API_URL}/menu", json=test_item)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], test_item["name"])
        self.assertEqual(data["price"], test_item["price"])
        self.assertEqual(data["category"], test_item["category"])
        self.assertTrue("id" in data)
        
        # Save the item ID for later tests
        self.item_id = data["id"]
        print(f"✅ Create menu item test passed (created item with ID: {self.item_id})")
        return data["id"]
    
    def test_04_get_all_menu_items(self):
        """Test getting all menu items"""
        response = requests.get(f"{API_URL}/menu")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # There should be at least one item (the one we just created)
        self.assertGreaterEqual(len(data), 1)
        print(f"✅ Get all menu items test passed (found {len(data)} items)")
    
    def test_05_get_menu_by_category(self):
        """Test getting menu items by category"""
        # Test appetizers category
        response = requests.get(f"{API_URL}/menu/category/appetizers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # All items should be in the appetizers category
        for item in data:
            self.assertEqual(item["category"], "appetizers")
        print(f"✅ Get menu by category (appetizers) test passed (found {len(data)} items)")
        
        # Test main_course category
        response = requests.get(f"{API_URL}/menu/category/main_course")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # All items should be in the main_course category
        for item in data:
            self.assertEqual(item["category"], "main_course")
        print(f"✅ Get menu by category (main_course) test passed (found {len(data)} items)")
    
    def test_06_create_order(self):
        """Test creating a new order"""
        # First, create a menu item to use in the order if we don't have one
        item_id = getattr(self, 'item_id', None)
        if not item_id:
            item_id = self.test_03_create_menu_item()
        
        # Create an order with the menu item
        test_order = {
            "customer_name": "Rahul Sharma",
            "customer_phone": "+91-9876543210",
            "customer_email": "rahul.sharma@example.com",
            "order_type": "delivery",
            "delivery_address": "123 Main St, Narsinghpur, MP",
            "special_notes": "Please make it less spicy",
            "items": [
                {
                    "menu_item_id": item_id,
                    "quantity": 2,
                    "special_instructions": "Extra onions please"
                }
            ]
        }
        
        response = requests.post(f"{API_URL}/orders", json=test_order)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["customer_name"], test_order["customer_name"])
        self.assertEqual(data["order_type"], test_order["order_type"])
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["menu_item_id"], item_id)
        self.assertEqual(data["items"][0]["quantity"], 2)
        self.assertTrue("total_amount" in data)
        self.assertTrue(data["total_amount"] > 0)
        print(f"✅ Create order test passed (total amount: ₹{data['total_amount']})")
    
    def test_07_get_all_orders(self):
        """Test getting all orders"""
        response = requests.get(f"{API_URL}/orders")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        # There should be at least one order (the one we just created)
        self.assertGreaterEqual(len(data), 1)
        print(f"✅ Get all orders test passed (found {len(data)} orders)")

if __name__ == "__main__":
    # Run the tests in order
    unittest.main(argv=['first-arg-is-ignored'], exit=False)