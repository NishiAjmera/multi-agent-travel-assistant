#!/usr/bin/env python3
"""
Main server file for Travel Booking Agent using A2A Protocol
Integrates flights and hotels agents with Google's Agent 2 Agent framework
"""

import os
import uvicorn
from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a_flights import flights_agent_card

# Import our custom components
# from agents import public_agent_card, specific_extended_agent_card
from flights_agent_executor import FlightsAgentExecutor
# from agent_executor import TravelAgentExecutor

def create_server():
    """
    Create and configure the A2A Starlette application server
    """
    # Initialize the request handler with our custom agent executor
    request_handler = DefaultRequestHandler(
        agent_executor=FlightsAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create the A2A Starlette application
    server = A2AStarletteApplication(
        agent_card=flights_agent_card,
        http_handler=request_handler,
        # extended_agent_card=specific_extended_agent_card,
    )
    
    return server

def main():
    """
    Main function to start the server
    """
    
    # Validate environment variables

    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    
    # if os.getenv("OPENAI_BASE_URL"):
    #     print(f"Using enterprise OpenAI base URL: {os.getenv('OPENAI_BASE_URL')}")
    
    # Create the server
    print("🚀 Starting Travel Booking Agent Server...")
    print("📍 Server will be available at: http://localhost:9999")
    print("🔍 Agent discovery endpoint: http://localhost:9999/a2a/discover")
    print("📋 Available agents: flights, hotels")
    print("✈️  Flight Agent URL: http://localhost:9999/agents/flights") 
    print("🏨 Hotel Agent URL: http://localhost:9999/agents/hotels")
    print()
    
    server = create_server()
    
    # Start the server
    uvicorn.run(
        server.build(), 
        host='0.0.0.0', 
        port=9999,
        log_level="info"
    )

if __name__ == "__main__":
    main()