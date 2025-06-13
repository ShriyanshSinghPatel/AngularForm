from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Shriyansh Restaurant API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Restaurant Models
class MenuCategory(str, Enum):
    APPETIZERS = "appetizers"
    MAIN_COURSE = "main_course"
    BREADS = "breads"
    RICE = "rice"
    BEVERAGES = "beverages"
    DESSERTS = "desserts"
    SNACKS = "snacks"

class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: MenuCategory
    is_available: bool = True
    is_spicy: bool = False
    preparation_time: int = 15  # in minutes
    ingredients: List[str] = []
    image_url: Optional[str] = None

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: MenuCategory
    is_available: bool = True
    is_spicy: bool = False
    preparation_time: int = 15
    ingredients: List[str] = []
    image_url: Optional[str] = None

class RestaurantInfo(BaseModel):
    name: str = "Shriyansh Restaurant"
    description: str = "Authentic Pure Vegetarian Indian Cuisine"
    address: str = "Narsinghpur, Madhya Pradesh, India"
    phone: str = "+91-XXXXXXXXXX"
    email: str = "info@shriyanshrestaurant.com"
    opening_hours: dict = {
        "monday": "11:00 AM - 10:00 PM",
        "tuesday": "11:00 AM - 10:00 PM", 
        "wednesday": "11:00 AM - 10:00 PM",
        "thursday": "11:00 AM - 10:00 PM",
        "friday": "11:00 AM - 10:00 PM",
        "saturday": "11:00 AM - 11:00 PM",
        "sunday": "11:00 AM - 11:00 PM"
    }
    services: List[str] = ["Takeout", "Delivery", "Catering"]
    specialties: List[str] = ["Pure Vegetarian", "North Indian", "Traditional Recipes"]

class OrderItem(BaseModel):
    menu_item_id: str
    quantity: int
    special_instructions: str = ""

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    customer_phone: str
    customer_email: str = ""
    items: List[OrderItem]
    total_amount: float
    order_type: str  # "takeout", "delivery", "catering"
    status: str = "pending"  # "pending", "confirmed", "preparing", "ready", "delivered"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    delivery_address: str = ""
    special_notes: str = ""

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str = ""
    items: List[OrderItem]
    order_type: str
    delivery_address: str = ""
    special_notes: str = ""

# Restaurant API Routes
@api_router.get("/")
async def root():
    return {"message": "Welcome to Shriyansh Restaurant API"}

@api_router.get("/restaurant-info", response_model=RestaurantInfo)
async def get_restaurant_info():
    """Get restaurant information"""
    return RestaurantInfo()

@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu():
    """Get all menu items"""
    menu_items = await db.menu_items.find().to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.get("/menu/category/{category}", response_model=List[MenuItem])
async def get_menu_by_category(category: MenuCategory):
    """Get menu items by category"""
    menu_items = await db.menu_items.find({"category": category.value}).to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.post("/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate):
    """Create a new menu item"""
    menu_item = MenuItem(**item.dict())
    await db.menu_items.insert_one(menu_item.dict())
    return menu_item

@api_router.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: str, item: MenuItemCreate):
    """Update a menu item"""
    updated_item = await db.menu_items.find_one_and_update(
        {"id": item_id},
        {"$set": item.dict()},
        return_document=True
    )
    if not updated_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return MenuItem(**updated_item)

@api_router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: str):
    """Delete a menu item"""
    result = await db.menu_items.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully"}

@api_router.post("/orders", response_model=Order)
async def create_order(order: OrderCreate):
    """Create a new order"""
    # Calculate total amount
    total_amount = 0.0
    for item in order.items:
        menu_item = await db.menu_items.find_one({"id": item.menu_item_id})
        if menu_item:
            total_amount += menu_item["price"] * item.quantity
    
    order_obj = Order(**order.dict(), total_amount=total_amount)
    await db.orders.insert_one(order_obj.dict())
    return order_obj

@api_router.get("/orders", response_model=List[Order])
async def get_orders():
    """Get all orders"""
    orders = await db.orders.find().sort("created_at", -1).to_list(1000)
    return [Order(**order) for order in orders]

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get specific order"""
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
