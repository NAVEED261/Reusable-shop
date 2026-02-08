#!/usr/bin/env python3
"""
Generate and store product embeddings in Qdrant vector database
"""

import os
import sys
import logging
from pathlib import Path

# Add backend path to imports
sys.path.insert(0, str(Path(__file__).parent.parent / "learnflow-app" / "app" / "backend" / "chat-service"))

import asyncio
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for all products in database."""

    def __init__(self):
        """Initialize database and RAG connections."""
        self.db_url = os.getenv("DATABASE_URL")
        self.qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

    def get_db_connection(self):
        """Connect to PostgreSQL database."""
        try:
            conn = psycopg2.connect(self.db_url)
            logger.info("Connected to PostgreSQL database")
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def fetch_products(self, conn):
        """Fetch all products from database."""
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.name, p.description, c.name as category, p.price, p.image_url
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.is_active = true
                ORDER BY p.id
            """)
            products = cursor.fetchall()
            cursor.close()
            logger.info(f"Fetched {len(products)} products from database")
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise

    def generate_embeddings(self):
        """Generate embeddings for all products."""
        try:
            # Import RAG client
            from rag_client import ProductRAGClient

            logger.info("=" * 70)
            logger.info("[EMBEDDING GENERATOR] GENERATING PRODUCT EMBEDDINGS")
            logger.info("=" * 70)

            # Initialize RAG client
            logger.info(f"Connecting to Qdrant at {self.qdrant_host}:{self.qdrant_port}")
            rag_client = ProductRAGClient(
                qdrant_host=self.qdrant_host,
                qdrant_port=self.qdrant_port,
                openai_api_key=self.openai_api_key
            )

            # Get database connection
            conn = self.get_db_connection()

            # Fetch products
            products = self.fetch_products(conn)

            if not products:
                logger.warning("No products found in database!")
                conn.close()
                return

            # Generate embeddings
            logger.info(f"\nGenerating embeddings for {len(products)} products...\n")

            success_count = 0
            error_count = 0

            for i, product in enumerate(products, 1):
                product_id, name, description, category, price, image_url = product

                try:
                    # Add product to Qdrant with embeddings
                    result = rag_client.add_product(
                        product_id=product_id,
                        name=name,
                        description=description or "",
                        category=category or "Other",
                        price=float(price) if price else 0.0,
                        image_url=image_url
                    )

                    if result:
                        success_count += 1
                        logger.info(f"[{i}/{len(products)}] OK - {name}")
                    else:
                        error_count += 1
                        logger.error(f"[{i}/{len(products)}] FAIL - {name}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"[{i}/{len(products)}] ERROR - {name}: {e}")

            # Get collection stats
            conn.close()
            collection_info = rag_client.get_collection_info()

            # Print summary
            logger.info("\n" + "=" * 70)
            logger.info("[SUCCESS] EMBEDDING GENERATION COMPLETE")
            logger.info("=" * 70)
            logger.info(f"\nResults:")
            logger.info(f"  Successfully embedded: {success_count}")
            logger.info(f"  Failed: {error_count}")
            logger.info(f"  Total processed: {len(products)}")

            if collection_info:
                logger.info(f"\nQdrant Collection Info:")
                logger.info(f"  Collection: {collection_info.get('name', 'N/A')}")
                logger.info(f"  Total vectors: {collection_info.get('vectors_count', 0)}")
                logger.info(f"  Total points: {collection_info.get('points_count', 0)}")

            logger.info("\nEmbedding generation complete. RAG system ready for use.")

            return success_count, error_count

        except ImportError as e:
            logger.error(f"Failed to import RAG client: {e}")
            logger.error("Make sure you're running from correct directory")
            raise
        except Exception as e:
            logger.error(f"Error during embedding generation: {e}")
            raise

def main():
    """Main execution."""
    try:
        generator = EmbeddingGenerator()
        generator.generate_embeddings()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
