"""
Trip Budget Agent Main Entry Point

Summary:
This module serves as the main entry point for the Trip Budget Agent application.
It orchestrates the initialization of the MCP client and LangChain agent.

Description:
- Imports MCP client and agent creation functions.
- Sets up structured logging for application flow.
- Initializes the MCP client connection.
- Creates the LangChain agent with MCP tools.
- Provides a main execution loop for processing user queries.
- Handles graceful shutdown and resource cleanup.

If initialization or execution fails, errors are logged with stack trace details
and appropriate cleanup is performed.
"""
import asyncio
from langchain_core.messages import HumanMessage
from logger_config import setup_logger
from client import client
from agent import create_budget_agent

logger = setup_logger(__name__)


async def main():
    """
    Summary:
        Main execution function that initializes the agent and processes queries.
    
    Returns:
        None
    """
    logger.info("Starting Trip Budget Agent application")
    
    try:
        # Create the agent with MCP tools
        logger.debug("Initializing budget agent")
        agent = await create_budget_agent(client)
        logger.info("Agent initialized successfully")
        
        # Example queries - you can modify this section
        logger.info("Agent ready to process queries")
        
        # Example 1: Calculate food costs
        logger.info("Processing example query: food cost calculation")
        result = await agent.ainvoke({
            "messages": [HumanMessage(content="Calculate food cost for 5 days at 500 rupees per day")]
        })
        logger.info(f"Food cost result: {result}")
        print("\n" + "="*50)
        print("FOOD COST CALCULATION:")
        print("="*50)
        print(result.get('output', result))
        
        # Example 2: Calculate hotel costs
        logger.info("Processing example query: hotel cost calculation")
        result = await agent.ainvoke({
            "messages": [HumanMessage(content="Calculate hotel cost for 4 nights at 2000 rupees per night")]
        })
        logger.info(f"Hotel cost result: {result}")
        print("\n" + "="*50)
        print("HOTEL COST CALCULATION:")
        print("="*50)
        print(result.get('output', result))
        
        # Example 3: Calculate transport costs
        logger.info("Processing example query: transport cost calculation")
        result = await agent.ainvoke({
            "messages": [HumanMessage(content="Calculate transport cost for 300 km by train")]
        })
        logger.info(f"Transport cost result: {result}")
        print("\n" + "="*50)
        print("TRANSPORT COST CALCULATION:")
        print("="*50)
        print(result.get('output', result))
        
        # Example 4: Get total budget
        logger.info("Processing example query: total budget summary")
        result = await agent.ainvoke({
            "messages": [HumanMessage(content="Show me the total trip budget summary")]
        })
        logger.info(f"Total budget result: {result}")
        print("\n" + "="*50)
        print("TOTAL BUDGET SUMMARY:")
        print("="*50)
        print(result.get('output', result))
        
        logger.info("All example queries processed successfully")
        
    except Exception:
        logger.exception("Error in main execution")
        raise
    
    finally:
        logger.info("Trip Budget Agent application shutting down")


async def interactive_mode():
    """
    Summary:
        Interactive mode for processing user queries in real-time.
    
    Returns:
        None
    """
    logger.info("Starting Trip Budget Agent in interactive mode")
    
    try:
        # Create the agent
        logger.debug("Initializing corporate agent for interactive mode")
        agent = await create_budget_agent(client)
        logger.info("Agent initialized successfully")
        
        print("\n" + "="*60)
        print("🌍 TRIP BUDGET AGENT - INTERACTIVE MODE")
        print("="*60)
        print("Available commands:")
        print("  - Calculate food, hotel, or transport costs")
        print("  - Get total budget summary")
        print("  - Clear all expenses")
        print("  - Type 'exit' or 'quit' to end session")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    logger.info("User requested exit")
                    print("\n👋 Goodbye! Safe travels!")
                    break
                
                if not user_input:
                    continue
                
                logger.info(f"Processing user query: {user_input}")
                result = await agent.ainvoke({
                    "messages": [HumanMessage(content=user_input)]
                })
                
                output = result.get('output', result)
                print(f"\n🤖 Agent: {output}")
                logger.debug(f"Agent response: {output}")
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                logger.exception("Error processing query in interactive mode")
                print(f"\n❌ Error: {str(e)}")
                print("Please try again with a different query.")
        
    except Exception:
        logger.exception("Error in interactive mode")
        raise
    
    finally:
        logger.info("Interactive mode session ended")


if __name__ == "__main__":
    import sys
    
    logger.info("Trip Budget Agent starting")
    logger.debug(f"Command line arguments: {sys.argv}")
    
    # Check if interactive mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        logger.info("Running in interactive mode")
        asyncio.run(interactive_mode())
    else:
        logger.info("Running example queries")
        asyncio.run(main())
    
    logger.info("Trip Budget Agent terminated")