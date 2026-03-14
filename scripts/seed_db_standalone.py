"""
Standalone seed script - uses raw SQLAlchemy to avoid sqlmodel compatibility issues.
Seeds the Neon PostgreSQL database with 40 products across 4 categories.
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Text,
    Numeric, Boolean, DateTime, ForeignKey, inspect
)
from sqlalchemy.orm import Session

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/learnflow"
)

# Fix for asyncpg/neon: remove channel_binding if present
clean_url = DATABASE_URL.replace("&channel_binding=require", "")

engine = create_engine(clean_url, echo=False, connect_args={"connect_timeout": 30})

metadata = MetaData()

# Define tables
categories_table = Table(
    "categories", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), unique=True, nullable=False),
    Column("description", Text, nullable=True),
    Column("image_url", String(500), nullable=True),
)

products_table = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("description", Text, nullable=True),
    Column("price", Numeric(10, 2), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=True),
    Column("image_url", String(500), nullable=True),
    Column("stock_quantity", Integer, default=0),
    Column("is_active", Boolean, default=True),
    Column("featured", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow),
)


def seed_database():
    """Populate database with 40 products across 4 categories."""

    # Create tables if they don't exist
    metadata.create_all(engine)
    print("Tables created/verified.")

    with engine.begin() as conn:
        # Clear existing data (products first due to FK)
        conn.execute(products_table.delete())
        conn.execute(categories_table.delete())
        print("Cleared existing data.")

        # Insert categories
        categories_data = [
            {
                "name": "Fancy Suits",
                "description": "Elegant and ornate suits for special occasions",
                "image_url": "/images/fancy-suits/fancy-suits-01.jpg"
            },
            {
                "name": "Shalwar Qameez",
                "description": "Traditional South Asian formal wear",
                "image_url": "/images/shalwar-qameez/shalwar-qameez-01.jpg"
            },
            {
                "name": "Cotton Suits",
                "description": "Comfortable and breathable cotton formal wear",
                "image_url": "/images/cotton-suits/cotton-suits-01.jpg"
            },
            {
                "name": "Designer Brands",
                "description": "Premium designer collection",
                "image_url": "/images/designer-brands/designer-brands-01.jpg"
            }
        ]

        result = conn.execute(categories_table.insert().returning(categories_table.c.id, categories_table.c.name), categories_data)
        cat_rows = result.fetchall()
        categories = {row.name: row.id for row in cat_rows}
        print(f"Inserted {len(categories)} categories: {list(categories.keys())}")

        now = datetime.utcnow()

        # Define all 40 products
        products_data = [
            # === Fancy Suits (10) ===
            {"name": "Royal Blue Fancy Suit", "description": "Luxurious royal blue suit with intricate embroidery", "price": Decimal("8500.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-01.jpg", "stock_quantity": 5, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Emerald Green Formal Suit", "description": "Rich emerald green with gold embellishments", "price": Decimal("7500.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-02.jpg", "stock_quantity": 4, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Maroon Wedding Suit", "description": "Deep maroon with traditional patterns", "price": Decimal("9000.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-03.jpg", "stock_quantity": 3, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Black Evening Suit", "description": "Sophisticated black suit for formal events", "price": Decimal("8000.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-04.jpg", "stock_quantity": 6, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Silver Grey Suit", "description": "Elegant silver grey with subtle shimmer", "price": Decimal("7800.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-05.jpg", "stock_quantity": 4, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Burgundy Celebration Suit", "description": "Rich burgundy for celebrations", "price": Decimal("8200.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-06.jpg", "stock_quantity": 5, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Navy Blue Premium Suit", "description": "Premium navy blue suit with fine details", "price": Decimal("9500.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-07.jpg", "stock_quantity": 3, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Gold Embroidered Suit", "description": "Luxurious suit with gold embroidery", "price": Decimal("10000.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-08.jpg", "stock_quantity": 2, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Teal Formal Suit", "description": "Modern teal suit with traditional elements", "price": Decimal("7900.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-09.jpg", "stock_quantity": 5, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Charcoal Dress Suit", "description": "Charcoal grey perfect for formal occasions", "price": Decimal("8100.00"), "category_id": categories["Fancy Suits"], "image_url": "/images/fancy-suits/fancy-suits-10.jpg", "stock_quantity": 4, "is_active": True, "featured": False, "created_at": now, "updated_at": now},

            # === Shalwar Qameez (10) ===
            {"name": "Traditional Cream Shalwar Qameez", "description": "Classic cream colored traditional wear", "price": Decimal("4500.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-01.jpg", "stock_quantity": 8, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "White Formal Shalwar Qameez", "description": "Pristine white for formal occasions", "price": Decimal("4800.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-02.jpg", "stock_quantity": 6, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Off-White Embroidered Qameez", "description": "Off-white with beautiful embroidery", "price": Decimal("5200.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-03.jpg", "stock_quantity": 5, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Light Green Traditional Wear", "description": "Light green with traditional patterns", "price": Decimal("4700.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-04.jpg", "stock_quantity": 7, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Pale Blue Shalwar Qameez", "description": "Soft pale blue traditional suit", "price": Decimal("4600.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-05.jpg", "stock_quantity": 6, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Beige Luxury Qameez", "description": "Elegant beige with luxury finish", "price": Decimal("5500.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-06.jpg", "stock_quantity": 4, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Sage Green Formal Wear", "description": "Sophisticated sage green traditional suit", "price": Decimal("5000.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-07.jpg", "stock_quantity": 5, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Champagne Shalwar Qameez", "description": "Luxurious champagne colored traditional wear", "price": Decimal("5800.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-08.jpg", "stock_quantity": 3, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Soft Pink Traditional Suit", "description": "Delicate soft pink for elegant look", "price": Decimal("4900.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-09.jpg", "stock_quantity": 6, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Ash Grey Formal Qameez", "description": "Modern ash grey formal traditional wear", "price": Decimal("5100.00"), "category_id": categories["Shalwar Qameez"], "image_url": "/images/shalwar-qameez/shalwar-qameez-10.jpg", "stock_quantity": 5, "is_active": True, "featured": False, "created_at": now, "updated_at": now},

            # === Cotton Suits (10) ===
            {"name": "White Cotton Business Suit", "description": "Pure white cotton for business wear", "price": Decimal("3500.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-01.jpg", "stock_quantity": 10, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Light Blue Cotton Formal", "description": "Comfortable light blue cotton suit", "price": Decimal("3300.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-02.jpg", "stock_quantity": 9, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Cream Cotton Comfort Suit", "description": "Breathable cream cotton for comfort", "price": Decimal("3400.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-03.jpg", "stock_quantity": 8, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Pale Green Cotton Suit", "description": "Fresh pale green cotton formal wear", "price": Decimal("3600.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-04.jpg", "stock_quantity": 7, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Off-White Premium Cotton", "description": "Premium off-white cotton suit", "price": Decimal("3800.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-05.jpg", "stock_quantity": 6, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Beige Linen Cotton Mix", "description": "Beige cotton-linen blend for elegance", "price": Decimal("4000.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-06.jpg", "stock_quantity": 5, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Ash Cotton Formal Suit", "description": "Ash grey pure cotton formal wear", "price": Decimal("3700.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-07.jpg", "stock_quantity": 7, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Soft Pink Cotton Suit", "description": "Soft pink cotton for casual formality", "price": Decimal("3500.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-08.jpg", "stock_quantity": 8, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Lavender Cotton Formal", "description": "Light lavender pure cotton suit", "price": Decimal("3600.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-09.jpg", "stock_quantity": 6, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Sage Cotton Professional Suit", "description": "Professional sage green cotton wear", "price": Decimal("3750.00"), "category_id": categories["Cotton Suits"], "image_url": "/images/cotton-suits/cotton-suits-10.jpg", "stock_quantity": 7, "is_active": True, "featured": True, "created_at": now, "updated_at": now},

            # === Designer Brands (10) ===
            {"name": "Armani Premium Suit", "description": "Italian designer Armani premium suit", "price": Decimal("15000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-01.jpg", "stock_quantity": 2, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Hugo Boss Executive", "description": "Hugo Boss executive formal wear", "price": Decimal("12000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-02.jpg", "stock_quantity": 3, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Versace Luxury Suit", "description": "Versace luxury designer suit", "price": Decimal("18000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-03.jpg", "stock_quantity": 1, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Ralph Lauren Premium", "description": "Ralph Lauren premium formal collection", "price": Decimal("13500.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-04.jpg", "stock_quantity": 2, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Tom Ford Signature", "description": "Tom Ford signature formal suit", "price": Decimal("16500.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-05.jpg", "stock_quantity": 2, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Gucci Designer Collection", "description": "Gucci designer formal collection", "price": Decimal("17000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-06.jpg", "stock_quantity": 1, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Burberry Heritage Suit", "description": "Burberry heritage formal suit", "price": Decimal("14000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-07.jpg", "stock_quantity": 2, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Dolce & Gabbana Elite", "description": "Dolce & Gabbana elite formal wear", "price": Decimal("15500.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-08.jpg", "stock_quantity": 2, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
            {"name": "Prada Contemporary", "description": "Prada contemporary formal suit", "price": Decimal("16000.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-09.jpg", "stock_quantity": 1, "is_active": True, "featured": True, "created_at": now, "updated_at": now},
            {"name": "Valentino Signature", "description": "Valentino signature formal collection", "price": Decimal("15800.00"), "category_id": categories["Designer Brands"], "image_url": "/images/designer-brands/designer-brands-10.jpg", "stock_quantity": 2, "is_active": True, "featured": False, "created_at": now, "updated_at": now},
        ]

        conn.execute(products_table.insert(), products_data)
        print(f"Inserted {len(products_data)} products.")

        # Verify counts
        from sqlalchemy import select, func
        total = conn.execute(select(func.count()).select_from(products_table)).scalar()
        cat_count = conn.execute(select(func.count()).select_from(categories_table)).scalar()

        print(f"\nVerification:")
        print(f"  Categories: {cat_count}")
        print(f"  Products: {total}")

        # Count per category
        for cat_name, cat_id in categories.items():
            count = conn.execute(
                select(func.count()).select_from(products_table).where(products_table.c.category_id == cat_id)
            ).scalar()
            print(f"  {cat_name}: {count} products")

    print(f"\nSuccessfully seeded database with {len(products_data)} products across {len(categories)} categories!")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
