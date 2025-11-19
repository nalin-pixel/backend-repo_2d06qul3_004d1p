"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class ClothingItem(BaseModel):
    """
    Clothing inventory items
    Collection name: "clothingitem"
    """
    name: str = Field(..., description="Item name, e.g., \"Denim Jacket\"")
    category: str = Field(..., description="Category, e.g., Tops, Bottoms, Outerwear")
    size: str = Field(..., description="Size label, e.g., S, M, L, 32, One-Size")
    color: str = Field(..., description="Primary color")
    quantity: int = Field(0, ge=0, description="Units in stock")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    brand: Optional[str] = Field(None, description="Brand name")
    price: Optional[float] = Field(None, ge=0, description="Unit price")
    location: Optional[str] = Field(None, description="Storage location or rack")
    notes: Optional[str] = Field(None, description="Any extra notes")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
