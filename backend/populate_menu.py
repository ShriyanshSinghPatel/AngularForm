#!/usr/bin/env python3
"""
Script to populate Shriyansh Restaurant menu with sample items
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def populate_menu():
    # MongoDB connection
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Clear existing menu items
    await db.menu_items.delete_many({})
    
    # Sample menu items for Shriyansh Restaurant
    menu_items = [
        # Appetizers
        {
            "id": "app-001",
            "name": "Paneer Tikka",
            "description": "Marinated cottage cheese cubes grilled in tandoor with bell peppers and onions",
            "price": 180.0,
            "category": "appetizers",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 20,
            "ingredients": ["Paneer", "Bell Peppers", "Onions", "Yogurt", "Spices"]
        },
        {
            "id": "app-002", 
            "name": "Samosa (2 pcs)",
            "description": "Crispy deep-fried pastry filled with spiced potatoes and green peas",
            "price": 40.0,
            "category": "appetizers",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 10,
            "ingredients": ["Potatoes", "Green Peas", "Flour", "Spices"]
        },
        {
            "id": "app-003",
            "name": "Chaat Papdi",
            "description": "Crispy wafers topped with yogurt, chutneys, and spices",
            "price": 60.0,
            "category": "appetizers",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 10,
            "ingredients": ["Papdi", "Yogurt", "Tamarind Chutney", "Mint Chutney", "Spices"]
        },
        
        # Main Course
        {
            "id": "main-001",
            "name": "Dal Makhani",
            "description": "Rich and creamy black lentils slow-cooked with butter and cream",
            "price": 160.0,
            "category": "main_course",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 25,
            "ingredients": ["Black Lentils", "Butter", "Cream", "Tomatoes", "Spices"]
        },
        {
            "id": "main-002",
            "name": "Paneer Butter Masala",
            "description": "Cottage cheese cubes in rich tomato-based creamy gravy",
            "price": 200.0,
            "category": "main_course",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 20,
            "ingredients": ["Paneer", "Tomatoes", "Butter", "Cream", "Spices"]
        },
        {
            "id": "main-003",
            "name": "Palak Paneer",
            "description": "Fresh cottage cheese cooked in creamy spinach gravy",
            "price": 180.0,
            "category": "main_course",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 20,
            "ingredients": ["Paneer", "Spinach", "Cream", "Onions", "Spices"]
        },
        {
            "id": "main-004",
            "name": "Chole Bhature",
            "description": "Spiced chickpeas served with fluffy deep-fried bread",
            "price": 120.0,
            "category": "main_course",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 15,
            "ingredients": ["Chickpeas", "Flour", "Spices", "Onions", "Tomatoes"]
        },
        {
            "id": "main-005",
            "name": "Aloo Gobi",
            "description": "Dry curry with potatoes and cauliflower cooked with aromatic spices",
            "price": 140.0,
            "category": "main_course",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 20,
            "ingredients": ["Potatoes", "Cauliflower", "Turmeric", "Spices"]
        },
        
        # Breads
        {
            "id": "bread-001",
            "name": "Butter Naan",
            "description": "Soft leavened bread brushed with butter, baked in tandoor",
            "price": 50.0,
            "category": "breads",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 10,
            "ingredients": ["Flour", "Yogurt", "Butter", "Yeast"]
        },
        {
            "id": "bread-002",
            "name": "Garlic Naan",
            "description": "Naan bread topped with fresh garlic and cilantro",
            "price": 60.0,
            "category": "breads",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 12,
            "ingredients": ["Flour", "Garlic", "Cilantro", "Butter"]
        },
        {
            "id": "bread-003",
            "name": "Tandoori Roti",
            "description": "Whole wheat bread cooked in tandoor",
            "price": 30.0,
            "category": "breads",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 8,
            "ingredients": ["Whole Wheat Flour", "Water", "Salt"]
        },
        {
            "id": "bread-004",
            "name": "Stuffed Paratha",
            "description": "Layered bread stuffed with spiced potatoes",
            "price": 70.0,
            "category": "breads",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 15,
            "ingredients": ["Wheat Flour", "Potatoes", "Spices", "Ghee"]
        },
        
        # Rice
        {
            "id": "rice-001",
            "name": "Jeera Rice",
            "description": "Fragrant basmati rice cooked with cumin seeds",
            "price": 80.0,
            "category": "rice",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 15,
            "ingredients": ["Basmati Rice", "Cumin Seeds", "Ghee"]
        },
        {
            "id": "rice-002",
            "name": "Vegetable Biryani",
            "description": "Aromatic basmati rice layered with mixed vegetables and spices",
            "price": 150.0,
            "category": "rice",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 30,
            "ingredients": ["Basmati Rice", "Mixed Vegetables", "Saffron", "Spices"]
        },
        {
            "id": "rice-003",
            "name": "Pulao",
            "description": "Mildly spiced rice with vegetables and aromatic spices",
            "price": 100.0,
            "category": "rice",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 20,
            "ingredients": ["Basmati Rice", "Vegetables", "Whole Spices"]
        },
        
        # Beverages
        {
            "id": "bev-001",
            "name": "Masala Chai",
            "description": "Traditional Indian tea brewed with aromatic spices",
            "price": 25.0,
            "category": "beverages",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 5,
            "ingredients": ["Tea Leaves", "Milk", "Ginger", "Cardamom", "Spices"]
        },
        {
            "id": "bev-002",
            "name": "Sweet Lassi",
            "description": "Refreshing yogurt-based drink with sugar and cardamom",
            "price": 40.0,
            "category": "beverages",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 5,
            "ingredients": ["Yogurt", "Sugar", "Cardamom", "Ice"]
        },
        {
            "id": "bev-003",
            "name": "Mango Lassi",
            "description": "Creamy mango flavored yogurt drink",
            "price": 50.0,
            "category": "beverages",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 5,
            "ingredients": ["Yogurt", "Mango Pulp", "Sugar", "Ice"]
        },
        {
            "id": "bev-004",
            "name": "Fresh Lime Water",
            "description": "Refreshing lime juice with sugar and mint",
            "price": 30.0,
            "category": "beverages",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 3,
            "ingredients": ["Fresh Lime", "Sugar", "Mint", "Water"]
        },
        
        # Desserts
        {
            "id": "des-001",
            "name": "Gulab Jamun (2 pcs)",
            "description": "Soft milk dumplings soaked in rose-flavored sugar syrup",
            "price": 60.0,
            "category": "desserts",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 10,
            "ingredients": ["Milk Powder", "Flour", "Sugar", "Rose Water", "Cardamom"]
        },
        {
            "id": "des-002",
            "name": "Kulfi",
            "description": "Traditional Indian ice cream made with condensed milk and nuts",
            "price": 45.0,
            "category": "desserts",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 5,
            "ingredients": ["Milk", "Sugar", "Nuts", "Cardamom"]
        },
        {
            "id": "des-003",
            "name": "Kheer",
            "description": "Rice pudding cooked with milk, sugar, and nuts",
            "price": 50.0,
            "category": "desserts",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 15,
            "ingredients": ["Rice", "Milk", "Sugar", "Nuts", "Cardamom"]
        },
        
        # Snacks
        {
            "id": "snack-001",
            "name": "Pav Bhaji",
            "description": "Spiced vegetable curry served with buttered bread rolls",
            "price": 80.0,
            "category": "snacks",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 15,
            "ingredients": ["Mixed Vegetables", "Pav Bread", "Butter", "Spices"]
        },
        {
            "id": "snack-002",
            "name": "Dosa",
            "description": "Crispy South Indian crepe served with coconut chutney and sambar",
            "price": 70.0,
            "category": "snacks",
            "is_available": True,
            "is_spicy": False,
            "preparation_time": 12,
            "ingredients": ["Rice", "Lentils", "Coconut", "Curry Leaves"]
        },
        {
            "id": "snack-003",
            "name": "Poha",
            "description": "Flattened rice cooked with onions, turmeric, and mustard seeds",
            "price": 50.0,
            "category": "snacks",
            "is_available": True,
            "is_spicy": True,
            "preparation_time": 10,
            "ingredients": ["Flattened Rice", "Onions", "Turmeric", "Mustard Seeds"]
        }
    ]
    
    # Insert menu items
    result = await db.menu_items.insert_many(menu_items)
    print(f"Inserted {len(result.inserted_ids)} menu items successfully!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(populate_menu())