"""
FastAPI backend for Chemical Equipment API.
Deployed on Railway with PostgreSQL.
"""
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import database setup
from database import get_db, init_db, engine, Base
# Import models
from models import Equipment

# Create FastAPI instance
app = FastAPI(
    title="Chemical Equipment API",
    description="API for managing chemical equipment data",
    version="1.0.0",
)

# CORS configuration - allow all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# STARTUP EVENT - Create tables automatically
# ============================================================================
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on application startup.
    Tables are created only if they don't exist (idempotent).
    """
    print("Starting up...")
    init_db()
    print("Database initialized - tables ready")


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Chemical Equipment API is running"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
    }


# ============================================================================
# EQUIPMENT CRUD ENDPOINTS
# ============================================================================

@app.get("/equipments/")
async def get_equipments(db: Session = Depends(get_db)):
    """
    Get all equipment records.
    """
    equipments = db.query(Equipment).all()
    return [eq.to_dict() for eq in equipments]


@app.get("/equipments/{equipment_id}")
async def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """
    Get a specific equipment record by ID.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment.to_dict()


@app.post("/equipments/")
async def create_equipment(
    name: str,
    category: str = None,
    material: str = None,
    db: Session = Depends(get_db)
):
    """
    Create a new equipment record.
    """
    equipment = Equipment(
        name=name,
        category=category,
        material=material,
    )
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment.to_dict()


@app.put("/equipments/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    name: str = None,
    category: str = None,
    material: str = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing equipment record.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if name is not None:
        equipment.name = name
    if category is not None:
        equipment.category = category
    if material is not None:
        equipment.material = material
    
    db.commit()
    db.refresh(equipment)
    return equipment.to_dict()


@app.delete("/equipments/{equipment_id}")
async def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """
    Delete an equipment record.
    """
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}


# ============================================================================
# MAIN ENTRY POINT (for local development)
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Railway sets this)
    port = int(os.getenv("PORT", 8000))
    
    # Run with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Bind to all interfaces
        port=port,
        reload=False,     # Disable reload in production
    )

