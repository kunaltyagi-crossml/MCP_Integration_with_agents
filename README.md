# Trip Budget Calculator - MCP Agent

A FastMCP-based travel budget calculator agent with 4 core tools (plus 2 utility tools) for comprehensive trip expense management. Built with Python, SQLite, and Model Context Protocol (MCP) integration.

🌟 Overview

Trip Budget Calculator is an AI-powered expense management system that helps travelers plan and track their trip budgets intelligently. Built with Model Context Protocol (MCP) and LangChain, it provides a natural language interface for calculating food, accommodation, and transport costs with persistent SQLite storage.

✨ Key Features

- 🤖 AI-Powered Interface - Natural language queries powered by Google Gemini
- 💰 Multi-Category Tracking - Food, Hotel, and Transport expense management
- 🚗 Smart Transport Rates - Automatic rate calculation for Bus, Train, Cab, and Flight
- 💾 Persistent Storage - SQLite database for expense history
- 📊 Budget Summaries - Beautiful formatted reports with category-wise breakdown
- 🔧 MCP Integration - Built with FastMCP for tool-based agent architecture
- 🇮🇳 Indian Currency - Native support for INR (₹) calculations

🚀 Project Overview

This project demonstrates a single MCP agent with 6 specialized tools that work together to help users plan and track their trip expenses. The agent uses FastMCP for tool integration and SQLite for persistent storage of expense data.

### 🛠️ Core Tools Available

##### 1. food_cost - Food Cost Calculator

- Calculates total food expenses for the trip

- Parameters:

  - days (int): Number of days for the trip
  - cost_per_day (int): Food cost per day in INR

- Stores expense in database with description
- Returns: Dictionary with status, category, amount, currency, and details


##### 2. hotel_cost - Hotel Cost Calculator

- Calculates total accommodation expenses
- Parameters:

    - nights (int): Number of nights
    - price_per_night (int): Cost per night in INR

- Stores expense in database with description
- Returns: Dictionary with status, category, amount, currency, and details


##### 3. transport_cost - Transport Cost Calculator

- Calculates transport costs based on distance and type
- Parameters:

   - distance_km (int): Distance in kilometers
   - transport_type (str): Type of transport (bus, train, cab, flight)


**Rate structure:**

    - Bus: ₹2/km
    - Train: ₹1.5/km
    - Cab: ₹10/km
    - Flight: ₹6/km

- Stores expense in database with details
- Returns: Dictionary with status, category, amount, transport_type, distance_km, rate_per_km, currency, and details


##### 4. total_budget - Total Budget Summary

- Retrieves all expenses from database
- No parameters required
- Generates formatted budget breakdown
- Shows category-wise subtotals and grand total
- Returns: Formatted string with complete budget summary


**📊 Additional Tools**
 
The project also includes two utility tools:

 ##### clear_all_expenses

- Clears all expenses from the database
- Useful for starting a new trip calculation
- Returns success/error status with message

##### get_expense_summary

- Returns structured JSON with category-wise breakdown
- Includes total, categories with items and subtotals
- Alternative to the formatted text output from total_budgeT.


### Technology Stack

- Programming Language: Python 3.x
- MCP Framework: FastMCP
- Database: SQLite (trip_budget.db)
- Logging: Python logging module

 ### ⚙️ Setup Instructions
    
1. Clone the repository

```bash
    git clone <your-repository-url>
    cd <project-directory>
```
   
3. Create and activate a virtual environment (recommended)
   
```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
   
```bash
   pip install -r requirements.txt
```
   
4. Verify database creation
   
The database will be automatically created when you run the server for the first time.

**🎯 Usage**

Running the MCP Server

```bash
   python3 mcp_server.py
```

The server starts in stdio transport mode and is ready to accept tool calls.

**Example Queries**

- Calculate Food Expenses:

```bash
Calculate food cost for 5 days at ₹500 per day
```

- Calculate Hotel Expenses:

```bash
What's the hotel cost for 3 nights at ₹2000 per night?
```
- Calculate Transport Expenses:

```bash
Calculate transport cost for 250 km by train
```
- Get Total Budget:
  
```bash
Show me the total trip budget
```

**🎓 Learning Outcomes**

- Implementing MCP agents with FastMCP
- Designing modular tool architectures
- Managing persistent data with SQLite
- Creating user-friendly formatted outputs
- Building production-ready agent workflows
- Error handling and logging best practices

**🔮 Future Enhancements**

- Add more expense categories (Activities, Shopping, Miscellaneous)
- Implement budget limits and alerts
- Add currency conversion support
- Export budget reports to PDF/Excel
- Web UI for better visualization
- Multi-trip management
- Budget comparison and analytics
