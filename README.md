Trip Budget Calculator - MCP Agent

A FastMCP-based travel budget calculator agent with 4 core tools (plus 2 utility tools) for comprehensive trip expense management. Built with Python, SQLite, and Model Context Protocol (MCP) integration.
🚀 Project Overview
This project demonstrates a single MCP agent with 6 specialized tools that work together to help users plan and track their trip expenses. The agent uses FastMCP for tool integration and SQLite for persistent storage of expense data.
Tools Available

food_cost - Food Cost Calculator

Calculates total food expenses for the trip
Parameters:

days (int): Number of days for the trip
cost_per_day (int): Food cost per day in INR


Stores expense in database with description
Returns: Dictionary with status, category, amount, currency, and details


hotel_cost - Hotel Cost Calculator

Calculates total accommodation expenses
Parameters:

nights (int): Number of nights
price_per_night (int): Cost per night in INR


Stores expense in database with description
Returns: Dictionary with status, category, amount, currency, and details


transport_cost - Transport Cost Calculator

Calculates transport costs based on distance and type
Parameters:

distance_km (int): Distance in kilometers
transport_type (str): Type of transport (bus, train, cab, flight)


Rate structure:

Bus: ₹2/km
Train: ₹1.5/km
Cab: ₹10/km
Flight: ₹6/km


Stores expense in database with details
Returns: Dictionary with status, category, amount, transport_type, distance_km, rate_per_km, currency, and details


total_budget - Total Budget Summary

Retrieves all expenses from database
No parameters required
Generates formatted budget breakdown
Shows category-wise subtotals and grand total
Returns: Formatted string with complete budget summary



Additional Utility Tools

clear_all_expenses - Clear Expenses

Clears all expenses from the database
Useful for starting a new trip calculation
No parameters required
Returns: Dictionary with status and message


get_expense_summary - Expense Summary

Get structured summary of all expenses
No parameters required
Returns category-wise breakdown in JSON format
Returns: Dictionary with status, total, categories, and currency



🏗️ Architecture
┌─────────────────────────────────────────────────────────┐
│                     User Query                          │
│          "Calculate my trip budget for..."              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FastMCP Agent (mcp_server.py)              │
│                 Travel Budget Calculator                │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┬─────────────┐
        │            │            │              │             │
        ▼            ▼            ▼              ▼             ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────┐
│ food_cost   │ │ hotel_  │ │transport_│ │total_budget │ │ Utility  │
│             │ │ cost    │ │  cost    │ │             │ │  Tools   │
│ Calculate   │ │         │ │          │ │ Get full    │ │          │
│ food        │ │Calculate│ │Calculate │ │ budget      │ │- clear   │
│ expenses    │ │ hotel   │ │transport │ │ summary     │ │- summary │
└──────┬──────┘ └────┬────┘ └────┬─────┘ └──────┬──────┘ └─────┬────┘
       │             │           │               │              │
       └─────────────┴───────────┴───────────────┴──────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   SQLite DB     │
            │ trip_budget.db  │
            │                 │
            │ Table: trip_expenses         │
            │ ├─ id (INTEGER PK)           │
            │ ├─ category (TEXT)           │
            │ ├─ amount (INTEGER)          │
            │ ├─ description (TEXT)        │
            │ └─ created_at (TEXT)         │
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Formatted      │
            │  Budget Report  │
            │  with ₹ symbols │
            └─────────────────┘
Technology Stack

Programming Language: Python 3.x
MCP Framework: FastMCP
Database: SQLite (trip_budget.db)
Logging: Python logging module

⚙️ Setup Instructions
1. Clone the repository
bashgit clone <your-repository-url>
cd <project-directory>
2. Create and activate a virtual environment (recommended)
bashpython3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
3. Install dependencies
bashpip install -r requirements.txt
4. Verify database creation
The database will be automatically created when you run the server for the first time.
🎯 Usage
Running the MCP Server
bashpython3 mcp_server.py
The server starts in stdio transport mode and is ready to accept tool calls.
Example Queries
Calculate Food Expenses:
Calculate food cost for 5 days at ₹500 per day
Calculate Hotel Expenses:
What's the hotel cost for 3 nights at ₹2000 per night?
Calculate Transport Expenses:
Calculate transport cost for 250 km by train
Get Total Budget:
Show me the total trip budget
Tool Usage Examples
1. food_cost Tool
python# Input parameters
{
  "days": 5,
  "cost_per_day": 500
}

# Output
{
  "status": "success",
  "category": "Food",
  "amount": 2500,
  "currency": "INR",
  "details": "5 days × ₹500/day"
}
2. hotel_cost Tool
python# Input parameters
{
  "nights": 3,
  "price_per_night": 2000
}

# Output
{
  "status": "success",
  "category": "Hotel",
  "amount": 6000,
  "currency": "INR",
  "details": "3 nights × ₹2,000/night"
}
3. transport_cost Tool
python# Input parameters
{
  "distance_km": 250,
  "transport_type": "train"
}

# Output
{
  "status": "success",
  "category": "Transport",
  "amount": 375,
  "transport_type": "train",
  "distance_km": 250,
  "rate_per_km": 1.5,
  "currency": "INR",
  "details": "250 km × ₹1.5/km via train"
}
4. total_budget Tool
python# No parameters required

# Output (formatted string)
"""
╔══════════════════════════════════════╗
║      TRIP BUDGET SUMMARY             ║
╚══════════════════════════════════════╝

Food:
  • ₹2,500 (5 days @ ₹500)
  Subtotal: ₹2,500

Hotel:
  • ₹6,000 (3 nights @ ₹2000)
  Subtotal: ₹6,000

Transport:
  • ₹375 (250 km via train)
  Subtotal: ₹375

─────────────────────────────────────────
💰 TOTAL TRIP BUDGET: ₹8,875
─────────────────────────────────────────
"""
5. clear_all_expenses Tool
python# No parameters required

# Output
{
  "status": "success",
  "message": "All expenses have been cleared. Ready for a new trip!"
}
6. get_expense_summary Tool
python# No parameters required

# Output
{
  "status": "success",
  "total": 8875,
  "categories": {
    "Food": {
      "items": [{"amount": 2500, "description": "5 days @ ₹500"}],
      "subtotal": 2500
    },
    "Hotel": {
      "items": [{"amount": 6000, "description": "3 nights @ ₹2000"}],
      "subtotal": 6000
    },
    "Transport": {
      "items": [{"amount": 375, "description": "250 km via train"}],
      "subtotal": 375
    }
  },
  "currency": "INR"
}
Sample Output
╔══════════════════════════════════════╗
║      TRIP BUDGET SUMMARY             ║
╚══════════════════════════════════════╝

Food:
  • ₹2,500 (5 days @ ₹500)
  Subtotal: ₹2,500

Hotel:
  • ₹6,000 (3 nights @ ₹2000)
  Subtotal: ₹6,000

Transport:
  • ₹375 (250 km via train)
  Subtotal: ₹375

─────────────────────────────────────────
💰 TOTAL TRIP BUDGET: ₹8,875
─────────────────────────────────────────
🗄️ Database Schema
Table: trip_expenses
ColumnTypeDescriptionidINTEGERPrimary key (auto-increment)categoryTEXTExpense category (Food/Hotel/Transport)amountINTEGERExpense amount in INRdescriptionTEXTDetailed description of expensecreated_atTEXTTimestamp (ISO format)
📊 Additional Tools
The project also includes two utility tools:
clear_all_expenses

Clears all expenses from the database
Useful for starting a new trip calculation
Returns success/error status with message

get_expense_summary

Returns structured JSON with category-wise breakdown
Includes total, categories with items and subtotals
Alternative to the formatted text output from total_budget

🎓 Learning Outcomes

Implementing MCP agents with FastMCP
Designing modular tool architectures
Managing persistent data with SQLite
Creating user-friendly formatted outputs
Building production-ready agent workflows
Error handling and logging best practices

🔮 Future Enhancements

Add more expense categories (Activities, Shopping, Miscellaneous)
Implement budget limits and alerts
Add currency conversion support
Export budget reports to PDF/Excel
Web UI for better visualization
Multi-trip management
Budget comparison and analytics