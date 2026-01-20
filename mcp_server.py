import logging
import sqlite3
from datetime import datetime
from fastmcp import FastMCP

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Database configuration
DB_PATH = "trip_budget.db"


# Database functions
def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create the trip_expenses table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trip_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount INTEGER,
        description TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
    logger.info("Database tables created/verified")


def insert_expense(category, amount, description):
    """Insert a new expense into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO trip_expenses
        (category, amount, description, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (category, amount, description, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def fetch_all_expenses():
    """Fetch all expenses from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, amount, description FROM trip_expenses")
    rows = cursor.fetchall()

    conn.close()
    return rows


def clear_expenses():
    """Clear all expenses from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM trip_expenses")
    
    conn.commit()
    conn.close()


# Initialize database
create_tables()

# Create FastMCP server
mcp = FastMCP("Travel Budget Calculator")


@mcp.tool()
def food_cost(days: int, cost_per_day: int) -> dict:
    """
    Calculates total food expense for the trip and stores it in the database.

    Args:
        days: Number of days for the trip
        cost_per_day: Food cost per day in INR

    Returns:
        Dictionary containing status, category, and total amount
    """
    try:
        total = days * cost_per_day
        insert_expense("Food", total, f"{days} days @ ₹{cost_per_day}")
        logger.info(f"Food expense inserted: ₹{total}")
        
        return {
            "status": "success",
            "category": "Food",
            "amount": total,
            "currency": "INR",
            "details": f"{days} days × ₹{cost_per_day}/day"
        }
    except Exception as e:
        logger.exception("Error calculating food cost")
        return {
            "status": "error",
            "message": f"Failed to calculate food cost: {str(e)}"
        }


@mcp.tool()
def hotel_cost(nights: int, price_per_night: int) -> dict:
    """
    Calculates total hotel expense for the trip and stores it in the database.

    Args:
        nights: Number of nights
        price_per_night: Cost per night in INR

    Returns:
        Dictionary containing status, category, and total amount
    """
    try:
        total = nights * price_per_night
        insert_expense("Hotel", total, f"{nights} nights @ ₹{price_per_night}")
        logger.info(f"Hotel expense inserted: ₹{total}")
        
        return {
            "status": "success",
            "category": "Hotel",
            "amount": total,
            "currency": "INR",
            "details": f"{nights} nights × ₹{price_per_night}/night"
        }
    except Exception as e:
        logger.exception("Error calculating hotel cost")
        return {
            "status": "error",
            "message": f"Failed to calculate hotel cost: {str(e)}"
        }


@mcp.tool()
def transport_cost(distance_km: int, transport_type: str) -> dict:
    """
    Calculates transport cost based on distance and type, then stores it in the database.

    Args:
        distance_km: Distance in kilometers
        transport_type: Type of transport (bus, train, cab, flight)

    Returns:
        Dictionary containing status, category, and total amount
    """
    try:
        rates = {
            "bus": 2,
            "train": 1.5,
            "cab": 10,
            "flight": 6
        }

        rate = rates.get(transport_type.lower())
        if not rate:
            logger.warning(f"Invalid transport type: {transport_type}")
            return {
                "status": "error",
                "message": f"Invalid transport type '{transport_type}'. Valid options: bus, train, cab, flight"
            }

        cost = int(distance_km * rate)
        insert_expense("Transport", cost, f"{distance_km} km via {transport_type}")
        logger.info(f"Transport expense inserted: ₹{cost}")
        
        return {
            "status": "success",
            "category": "Transport",
            "amount": cost,
            "transport_type": transport_type,
            "distance_km": distance_km,
            "rate_per_km": rate,
            "currency": "INR",
            "details": f"{distance_km} km × ₹{rate}/km via {transport_type}"
        }
    except Exception as e:
        logger.exception("Error calculating transport cost")
        return {
            "status": "error",
            "message": f"Failed to calculate transport cost: {str(e)}"
        }


@mcp.tool()
def total_budget() -> str:
    """
    Retrieves all expenses from the database and returns a trip budget summary.

    Returns:
        Formatted string showing breakdown of all expenses and total amount
    """
    try:
        expenses = fetch_all_expenses()
        
        if not expenses:
            return "No expenses recorded yet. Start adding expenses to see your budget!"
        
        # Calculate totals by category
        category_totals = {}
        for category, amount, description in expenses:
            if category not in category_totals:
                category_totals[category] = []
            category_totals[category].append((amount, description))
        
        # Build the breakdown
        breakdown_lines = []
        grand_total = 0
        
        for category, items in category_totals.items():
            category_total = sum(amount for amount, _ in items)
            grand_total += category_total
            breakdown_lines.append(f"\n{category}:")
            for amount, description in items:
                breakdown_lines.append(f"  • ₹{amount:,} ({description})")
            breakdown_lines.append(f"  Subtotal: ₹{category_total:,}")
        
        breakdown = "\n".join(breakdown_lines)
        
        logger.info("Total budget calculated successfully")
        return f"""
╔══════════════════════════════════════╗
║      TRIP BUDGET SUMMARY             ║
╚══════════════════════════════════════╝
{breakdown}

─────────────────────────────────────────
💰 TOTAL TRIP BUDGET: ₹{grand_total:,}
─────────────────────────────────────────
"""
    except Exception as e:
        logger.exception("Error fetching total budget")
        return f"Error: Failed to fetch total budget - {str(e)}"


@mcp.tool()
def clear_all_expenses() -> dict:
    """
    Clears all expenses from the database (useful for starting a new trip calculation).

    Returns:
        Dictionary with status message
    """
    try:
        clear_expenses()
        logger.info("All expenses cleared")
        return {
            "status": "success",
            "message": "All expenses have been cleared. Ready for a new trip!"
        }
    except Exception as e:
        logger.exception("Error clearing expenses")
        return {
            "status": "error",
            "message": f"Failed to clear expenses: {str(e)}"
        }


@mcp.tool()
def get_expense_summary() -> dict:
    """
    Get a structured summary of all expenses with category-wise breakdown.

    Returns:
        Dictionary containing expenses grouped by category with totals
    """
    try:
        expenses = fetch_all_expenses()
        
        if not expenses:
            return {
                "status": "success",
                "total": 0,
                "categories": {},
                "message": "No expenses recorded"
            }
        
        # Group by category
        categories = {}
        total = 0
        
        for category, amount, description in expenses:
            total += amount
            if category not in categories:
                categories[category] = {
                    "items": [],
                    "subtotal": 0
                }
            categories[category]["items"].append({
                "amount": amount,
                "description": description
            })
            categories[category]["subtotal"] += amount
        
        return {
            "status": "success",
            "total": total,
            "categories": categories,
            "currency": "INR"
        }
    except Exception as e:
        logger.exception("Error getting expense summary")
        return {
            "status": "error",
            "message": f"Failed to get expense summary: {str(e)}"
        }


if __name__ == "__main__":
    logger.info("Starting Travel Budget FastMCP Server")
    logger.info(f"Database: {DB_PATH}")
    mcp.run(transport="stdio")