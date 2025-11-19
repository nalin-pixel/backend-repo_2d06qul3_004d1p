import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import ClothingItem

app = FastAPI(title="Cloth Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Cloth Management API is running"}

@app.get("/schema")
def get_schema():
    """Expose schemas to the UI tooling"""
    return {
        "clothingitem": ClothingItem.model_json_schema(),
    }

class ClothingItemCreate(ClothingItem):
    pass

class ClothingItemOut(ClothingItem):
    id: Optional[str] = None

@app.post("/api/items", response_model=dict)
def create_item(item: ClothingItemCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("clothingitem", item)
    return {"id": inserted_id}

@app.get("/api/items", response_model=List[ClothingItemOut])
def list_items(category: Optional[str] = None, color: Optional[str] = None, size: Optional[str] = None, search: Optional[str] = None, limit: int = 100):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if color:
        filter_dict["color"] = color
    if size:
        filter_dict["size"] = size
    if search:
        # Simple case-insensitive regex search on name and brand
        filter_dict["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"brand": {"$regex": search, "$options": "i"}},
            {"sku": {"$regex": search, "$options": "i"}},
        ]
    docs = get_documents("clothingitem", filter_dict, limit)

    # Normalize Mongo _id to id and convert datetime to isoformat strings
    out = []
    for d in docs:
        d_copy = {k: v for k, v in d.items() if k != "_id"}
        d_copy["id"] = str(d.get("_id"))
        for k in ["created_at", "updated_at"]:
            if k in d_copy and hasattr(d_copy[k], "isoformat"):
                d_copy[k] = d_copy[k].isoformat()
        out.append(d_copy)
    return out

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db as test_db
        
        if test_db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = test_db.name if hasattr(test_db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = test_db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
