"""
Seed script to populate Neon database with 40 products across 4 categories
Connects to Neon PostgreSQL and inserts product data
"""

import os
import sys
from decimal import Decimal
from sqlmodel import SQLModel, create_engine, Session

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'learnflow-app', 'app', 'backend', 'product-service'))

from app.models import Category, Product

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/learnflow")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"connect_timeout": 10}
)


def seed_database():
    """Populate database with products"""

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Clear existing data
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        # Define categories
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

        # Create categories
        categories = {}
        for cat_data in categories_data:
            cat = Category(**cat_data)
            session.add(cat)
            session.flush()
            categories[cat_data["name"]] = cat.id

        session.commit()

        # Define products (10 per category)
        products_data = [
            # Fancy Suits (10 products)
            {
                "name": "Royal Blue Fancy Suit",
                "description": "Luxurious royal blue suit with intricate embroidery",
                "price": Decimal("8500.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-01.jpg",
                "stock_quantity": 5,
                "featured": True
            },
            {
                "name": "Emerald Green Formal Suit",
                "description": "Rich emerald green with gold embellishments",
                "price": Decimal("7500.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-02.jpg",
                "stock_quantity": 4,
                "featured": True
            },
            {
                "name": "Maroon Wedding Suit",
                "description": "Deep maroon with traditional patterns",
                "price": Decimal("9000.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-03.jpg",
                "stock_quantity": 3,
                "featured": False
            },
            {
                "name": "Black Evening Suit",
                "description": "Sophisticated black suit for formal events",
                "price": Decimal("8000.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-04.jpg",
                "stock_quantity": 6,
                "featured": True
            },
            {
                "name": "Silver Grey Suit",
                "description": "Elegant silver grey with subtle shimmer",
                "price": Decimal("7800.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-05.jpg",
                "stock_quantity": 4,
                "featured": False
            },
            {
                "name": "Burgundy Celebration Suit",
                "description": "Rich burgundy for celebrations",
                "price": Decimal("8200.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-06.jpg",
                "stock_quantity": 5,
                "featured": False
            },
            {
                "name": "Navy Blue Premium Suit",
                "description": "Premium navy blue suit with fine details",
                "price": Decimal("9500.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-07.jpg",
                "stock_quantity": 3,
                "featured": True
            },
            {
                "name": "Gold Embroidered Suit",
                "description": "Luxurious suit with gold embroidery",
                "price": Decimal("10000.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-08.jpg",
                "stock_quantity": 2,
                "featured": True
            },
            {
                "name": "Teal Formal Suit",
                "description": "Modern teal suit with traditional elements",
                "price": Decimal("7900.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-09.jpg",
                "stock_quantity": 5,
                "featured": False
            },
            {
                "name": "Charcoal Dress Suit",
                "description": "Charcoal grey perfect for formal occasions",
                "price": Decimal("8100.00"),
                "category_id": categories["Fancy Suits"],
                "image_url": "/images/fancy-suits/fancy-suits-10.jpg",
                "stock_quantity": 4,
                "featured": False
            },

            # Shalwar Qameez (10 products)
            {
                "name": "Traditional Cream Shalwar Qameez",
                "description": "Classic cream colored traditional wear",
                "price": Decimal("4500.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-01.jpg",
                "stock_quantity": 8,
                "featured": True
            },
            {
                "name": "White Formal Shalwar Qameez",
                "description": "Pristine white for formal occasions",
                "price": Decimal("4800.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-02.jpg",
                "stock_quantity": 6,
                "featured": False
            },
            {
                "name": "Off-White Embroidered Qameez",
                "description": "Off-white with beautiful embroidery",
                "price": Decimal("5200.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-03.jpg",
                "stock_quantity": 5,
                "featured": True
            },
            {
                "name": "Light Green Traditional Wear",
                "description": "Light green with traditional patterns",
                "price": Decimal("4700.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-04.jpg",
                "stock_quantity": 7,
                "featured": False
            },
            {
                "name": "Pale Blue Shalwar Qameez",
                "description": "Soft pale blue traditional suit",
                "price": Decimal("4600.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-05.jpg",
                "stock_quantity": 6,
                "featured": False
            },
            {
                "name": "Beige Luxury Qameez",
                "description": "Elegant beige with luxury finish",
                "price": Decimal("5500.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-06.jpg",
                "stock_quantity": 4,
                "featured": True
            },
            {
                "name": "Sage Green Formal Wear",
                "description": "Sophisticated sage green traditional suit",
                "price": Decimal("5000.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-07.jpg",
                "stock_quantity": 5,
                "featured": False
            },
            {
                "name": "Champagne Shalwar Qameez",
                "description": "Luxurious champagne colored traditional wear",
                "price": Decimal("5800.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-08.jpg",
                "stock_quantity": 3,
                "featured": True
            },
            {
                "name": "Soft Pink Traditional Suit",
                "description": "Delicate soft pink for elegant look",
                "price": Decimal("4900.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-09.jpg",
                "stock_quantity": 6,
                "featured": False
            },
            {
                "name": "Ash Grey Formal Qameez",
                "description": "Modern ash grey formal traditional wear",
                "price": Decimal("5100.00"),
                "category_id": categories["Shalwar Qameez"],
                "image_url": "/images/shalwar-qameez/shalwar-qameez-10.jpg",
                "stock_quantity": 5,
                "featured": False
            },

            # Cotton Suits (10 products)
            {
                "name": "White Cotton Business Suit",
                "description": "Pure white cotton for business wear",
                "price": Decimal("3500.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-01.jpg",
                "stock_quantity": 10,
                "featured": True
            },
            {
                "name": "Light Blue Cotton Formal",
                "description": "Comfortable light blue cotton suit",
                "price": Decimal("3300.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-02.jpg",
                "stock_quantity": 9,
                "featured": False
            },
            {
                "name": "Cream Cotton Comfort Suit",
                "description": "Breathable cream cotton for comfort",
                "price": Decimal("3400.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-03.jpg",
                "stock_quantity": 8,
                "featured": False
            },
            {
                "name": "Pale Green Cotton Suit",
                "description": "Fresh pale green cotton formal wear",
                "price": Decimal("3600.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-04.jpg",
                "stock_quantity": 7,
                "featured": True
            },
            {
                "name": "Off-White Premium Cotton",
                "description": "Premium off-white cotton suit",
                "price": Decimal("3800.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-05.jpg",
                "stock_quantity": 6,
                "featured": False
            },
            {
                "name": "Beige Linen Cotton Mix",
                "description": "Beige cotton-linen blend for elegance",
                "price": Decimal("4000.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-06.jpg",
                "stock_quantity": 5,
                "featured": True
            },
            {
                "name": "Ash Cotton Formal Suit",
                "description": "Ash grey pure cotton formal wear",
                "price": Decimal("3700.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-07.jpg",
                "stock_quantity": 7,
                "featured": False
            },
            {
                "name": "Soft Pink Cotton Suit",
                "description": "Soft pink cotton for casual formality",
                "price": Decimal("3500.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-08.jpg",
                "stock_quantity": 8,
                "featured": False
            },
            {
                "name": "Lavender Cotton Formal",
                "description": "Light lavender pure cotton suit",
                "price": Decimal("3600.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-09.jpg",
                "stock_quantity": 6,
                "featured": False
            },
            {
                "name": "Sage Cotton Professional Suit",
                "description": "Professional sage green cotton wear",
                "price": Decimal("3750.00"),
                "category_id": categories["Cotton Suits"],
                "image_url": "/images/cotton-suits/cotton-suits-10.jpg",
                "stock_quantity": 7,
                "featured": True
            },

            # Designer Brands (10 products)
            {
                "name": "Armani Premium Suit",
                "description": "Italian designer Armani premium suit",
                "price": Decimal("15000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-01.jpg",
                "stock_quantity": 2,
                "featured": True
            },
            {
                "name": "Hugo Boss Executive",
                "description": "Hugo Boss executive formal wear",
                "price": Decimal("12000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-02.jpg",
                "stock_quantity": 3,
                "featured": True
            },
            {
                "name": "Versace Luxury Suit",
                "description": "Versace luxury designer suit",
                "price": Decimal("18000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-03.jpg",
                "stock_quantity": 1,
                "featured": True
            },
            {
                "name": "Ralph Lauren Premium",
                "description": "Ralph Lauren premium formal collection",
                "price": Decimal("13500.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-04.jpg",
                "stock_quantity": 2,
                "featured": False
            },
            {
                "name": "Tom Ford Signature",
                "description": "Tom Ford signature formal suit",
                "price": Decimal("16500.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-05.jpg",
                "stock_quantity": 2,
                "featured": True
            },
            {
                "name": "Gucci Designer Collection",
                "description": "Gucci designer formal collection",
                "price": Decimal("17000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-06.jpg",
                "stock_quantity": 1,
                "featured": True
            },
            {
                "name": "Burberry Heritage Suit",
                "description": "Burberry heritage formal suit",
                "price": Decimal("14000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-07.jpg",
                "stock_quantity": 2,
                "featured": False
            },
            {
                "name": "Dolce & Gabbana Elite",
                "description": "Dolce & Gabbana elite formal wear",
                "price": Decimal("15500.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-08.jpg",
                "stock_quantity": 2,
                "featured": False
            },
            {
                "name": "Prada Contemporary",
                "description": "Prada contemporary formal suit",
                "price": Decimal("16000.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-09.jpg",
                "stock_quantity": 1,
                "featured": True
            },
            {
                "name": "Valentino Signature",
                "description": "Valentino signature formal collection",
                "price": Decimal("15800.00"),
                "category_id": categories["Designer Brands"],
                "image_url": "/images/designer-brands/designer-brands-10.jpg",
                "stock_quantity": 2,
                "featured": False
            },
        ]

        # Add products to session
        for prod_data in products_data:
            product = Product(**prod_data)
            session.add(product)

        session.commit()
        print(f"✅ Successfully seeded database with {len(products_data)} products across {len(categories)} categories!")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        sys.exit(1)
