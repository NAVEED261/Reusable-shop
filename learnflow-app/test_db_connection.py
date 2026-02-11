#!/usr/bin/env python3
"""Test database connection and verify tables."""

import os
import sys
from sqlmodel import create_engine, Session, text

# Load environment
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_RiFw31LNbBeX@ep-withered-tooth-ahbaotjq-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    # Create engine
    engine = create_engine(DATABASE_URL, echo=False)

    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]
        print(f"✓ Database connection successful: {db_name}")

    # Check tables
    with engine.connect() as connection:
        result = connection.execute(
            text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """)
        )
        tables = [row[0] for row in result.fetchall()]
        print(f"\n✓ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")

    # Check product count
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM products;"))
        product_count = result.fetchone()[0]
        print(f"\n✓ Product count: {product_count}")

    # Check categories
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT c.id, c.name, COUNT(p.id) as product_count FROM categories c LEFT JOIN products p ON c.id = p.category_id GROUP BY c.id, c.name ORDER BY c.id;")
        )
        print("\n✓ Categories:")
        for row in result.fetchall():
            print(f"  - {row[1]}: {row[2]} products")

    # Check test user
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, email FROM users WHERE email='test@example.com';")
        )
        test_user = result.fetchone()
        if test_user:
            print(f"\n✓ Test user exists: {test_user[0]} - {test_user[1]}")
        else:
            print(f"\n⚠ Test user does not exist in database")

    print("\n✅ Database verification complete!")

except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)
