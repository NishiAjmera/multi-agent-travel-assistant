
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import os

# Define tools for Flights agent
def get_flights(departure: str = "NYC", destination: str = "LAX", date: str = "2024-07-01") -> str:
    """Get available flights between cities"""
    flights = [
        f"Flight AA101: {departure} to {destination} on {date} - $299",
        f"Flight UA202: {departure} to {destination} on {date} - $315",
        f"Flight DL303: {departure} to {destination} on {date} - $289"
    ]
    return f"Available flights: {', '.join(flights)}"

def book_flight(flight_number: str, passenger_name: str = "John Doe") -> str:
    """Book a specific flight"""
    return f"Flight {flight_number} successfully booked for {passenger_name}. Confirmation: FL{flight_number[-3:]}{passenger_name[:2].upper()}123"

# Define tools for Hotels agent
def get_hotels(city: str = "Los Angeles", checkin: str = "2024-07-01", checkout: str = "2024-07-03") -> str:
    """Get available hotels in a city"""
    hotels = [
        f"Marriott Downtown {city}: ${150}/night ({checkin} to {checkout})",
        f"Hilton Garden Inn {city}: ${120}/night ({checkin} to {checkout})",
        f"Holiday Inn Express {city}: ${95}/night ({checkin} to {checkout})"
    ]
    return f"Available hotels: {', '.join(hotels)}"

def book_hotel(hotel_name: str, guest_name: str = "John Doe", checkin: str = "2024-07-01", checkout: str = "2024-07-03") -> str:
    """Book a specific hotel"""
    return f"Hotel {hotel_name} successfully booked for {guest_name} from {checkin} to {checkout}. Confirmation: HT{hotel_name[:3].upper()}{guest_name[:2].upper()}456"

# =============================================================================
# AGENT CLASSES
# =============================================================================

class FlightsAgent:
    def __init__(self, openai_api_key: str, base_url: str = None):
        self.agent_card = flights_agent_card
        
        # Initialize OpenAI model
        self.model = ChatOpenAI(
            model="gpt-4o",
            api_key=openai_api_key,
            base_url=base_url,
            temperature=0
        )
        
        # Initialize memory
        self.memory = MemorySaver()
        
        # System instruction for flights agent
        system_instruction = """You are a helpful flight booking assistant with the following capabilities:
        1. Flight Search: Search for available flights between cities on specific dates
        2. Flight Booking: Book flights for passengers with confirmation details
        
        Always be helpful and provide clear information about flight options and booking confirmations.
        When searching flights, ask for departure city, destination city, and travel date if not provided.
        When booking flights, ask for flight number and passenger name if not provided.
        
        You are part of the Agent 2 Agent protocol and can collaborate with other agents for comprehensive travel planning."""
        
        # Create the agent with tools
        self.agent = create_react_agent(
            self.model,
            tools=[get_flights, book_flight],
            checkpointer=self.memory,
            state_modifier=system_instruction
        )
        
    async def run(self, query: str, thread_id: str = "flights_thread") -> str:
        """Execute the agent with the given query"""
        try:
            config = {"configurable": {"thread_id": thread_id}}
            response = await self.agent.ainvoke({"messages": [("user", query)]}, config=config)
            return response["messages"][-1].content
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    # def get_agent_card(self) -> AgentCard:
    #     """Return the agent card for A2A protocol"""
    #     return self.agent_card

class HotelsAgent:
    def __init__(self, openai_api_key: str, base_url: str = None):
        self.agent_card = hotels_agent_card
        
        # Initialize OpenAI model
        self.model = ChatOpenAI(
            model="gpt-4o",
            api_key=openai_api_key,
            base_url=base_url,
            temperature=0
        )
        
        # Initialize memory
        self.memory = MemorySaver()
        
        # System instruction for hotels agent
        system_instruction = """You are a helpful hotel booking assistant with the following capabilities:
        1. Hotel Search: Search for available hotels in cities based on dates
        2. Hotel Booking: Book hotel reservations for guests with confirmation details
        
        Always be helpful and provide clear information about hotel options and booking confirmations.
        When searching hotels, ask for city, check-in date, and check-out date if not provided.
        When booking hotels, ask for hotel name, guest name, and dates if not provided.
        
        You are part of the Agent 2 Agent protocol and can collaborate with other agents for comprehensive travel planning."""
        
        # Create the agent with tools
        self.agent = create_react_agent(
            self.model,
            tools=[get_hotels, book_hotel],
            checkpointer=self.memory,
            state_modifier=system_instruction
        )
        
    async def run(self, query: str, thread_id: str = "hotels_thread") -> str:
        """Execute the agent with the given query"""
        try:
            config = {"configurable": {"thread_id": thread_id}}
            response = await self.agent.ainvoke({"messages": [("user", query)]}, config=config)
            return response["messages"][-1].content
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    # def get_agent_card(self) -> AgentCard:
    #     """Return the agent card for A2A protocol"""
    #     return self.agent_card

# =============================================================================
# COMBINED TRAVEL AGENT CARD (PUBLIC CARD)
# =============================================================================

# Combined skills for the public agent card
# combined_skills = [flights_skill1, flights_skill2, hotels_skill1, hotels_skill2]

# # Public agent card that represents the combined travel agent system
# public_agent_card = AgentCard(
#     name='Travel Booking Agent',
#     description='Comprehensive AI travel agent that can handle both flight and hotel bookings. Specialized in searching for and booking flights and accommodations with complete confirmation services.',
#     url='http://localhost:9999/',
#     version='1.0.0',
#     defaultInputModes=['text'],
#     defaultOutputModes=['text'],
#     capabilities=AgentCapabilities(streaming=True),
#     skills=combined_skills
# )

# # Extended agent card with additional metadata
# specific_extended_agent_card = {
#     "agents": {
#         "flights": flights_agent_card.dict(),
#         "hotels": hotels_agent_card.dict()
#     },
#     "coordination": {
#         "can_collaborate": True,
#         "supports_multi_step_planning": True,
#         "cross_agent_communication": True
#     },
#     "specializations": [
#         "flight_search_and_booking",
#         "hotel_search_and_booking", 
#         "travel_planning",
#         "reservation_management"
#     ]
# }