from a2a.agent_executor import AgentExecutor
from a2a.types import AgentInput, AgentOutput
from agents import FlightsAgent, HotelsAgent
import os
import json
import asyncio
from typing import AsyncGenerator, Dict, Any

class TravelAgentExecutor(AgentExecutor):
    """
    A2A Agent Executor for the Travel Booking System
    Handles both flights and hotels booking requests
    """
    
    def __init__(self):
        # Initialize the individual agents
        openai_api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        
        self.flights_agent = FlightsAgent(openai_api_key, openai_base_url)
        self.hotels_agent = HotelsAgent(openai_api_key, openai_base_url)
        
        # Keywords to route requests to appropriate agents
        self.flight_keywords = [
            'flight', 'flights', 'fly', 'airplane', 'airline', 'departure', 
            'arrival', 'airport', 'boarding', 'ticket', 'aviation'
        ]
        
        self.hotel_keywords = [
            'hotel', 'hotels', 'accommodation', 'room', 'stay', 'lodge', 
            'resort', 'inn', 'booking', 'reservation', 'check-in', 'check-out'
        ]
    
    def _determine_agent_type(self, query: str) -> str:
        """
        Determine which agent should handle the query based on keywords
        """
        query_lower = query.lower()
        
        flight_score = sum(1 for keyword in self.flight_keywords if keyword in query_lower)
        hotel_score = sum(1 for keyword in self.hotel_keywords if keyword in query_lower)
        
        if flight_score > hotel_score:
            return "flights"
        elif hotel_score > flight_score:
            return "hotels"
        else:
            # If unclear, try to handle both or ask for clarification
            return "both"
    
    async def execute(self, agent_input: AgentInput) -> AsyncGenerator[AgentOutput, None]:
        """
        Execute the agent based on the input
        """
        try:
            # Extract the query from the input
            if hasattr(agent_input, 'messages') and agent_input.messages:
                query = agent_input.messages[-1].content
            elif hasattr(agent_input, 'text'):
                query = agent_input.text
            else:
                query = str(agent_input)
            
            # Determine which agent to use
            agent_type = self._determine_agent_type(query)
            
            if agent_type == "flights":
                result = self.flights_agent.run(query)
                yield AgentOutput(
                    text=result,
                    metadata={
                        "agent_used": "flights",
                        "agent_type": "flight-booking",
                        "skills_used": ["flight-search", "flight-booking"]
                    }
                )
            elif agent_type == "hotels":
                result = self.hotels_agent.run(query)
                yield AgentOutput(
                    text=result,
                    metadata={
                        "agent_used": "hotels", 
                        "agent_type": "hotel-booking",
                        "skills_used": ["hotel-search", "hotel-booking"]
                    }
                )
            else:
                # Handle both or ask for clarification
                response = """I'm a travel booking agent that can help with both flights and hotels. 
                
Could you please specify whether you're looking for:
- Flight booking (search and book flights between cities)
- Hotel booking (search and book accommodations)
- Or if you need help with both, I can assist with a complete travel plan!

Just let me know what you'd like to do."""
                
                yield AgentOutput(
                    text=response,
                    metadata={
                        "agent_used": "coordinator",
                        "agent_type": "travel-coordinator", 
                        "skills_available": ["flight-search", "flight-booking", "hotel-search", "hotel-booking"],
                        "clarification_needed": True
                    }
                )
                
        except Exception as e:
            error_message = f"Error processing your request: {str(e)}"
            yield AgentOutput(
                text=error_message,
                metadata={
                    "error": True,
                    "error_type": "execution_error",
                    "error_message": str(e)
                }
            )
    
    async def execute_streaming(self, agent_input: AgentInput) -> AsyncGenerator[AgentOutput, None]:
        """
        Execute with streaming support
        """
        async for output in self.execute(agent_input):
            yield output
            # Add a small delay to simulate streaming
            await asyncio.sleep(0.1)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this agent executor
        """
        return {
            "supports_streaming": True,
            "supports_flights": True,
            "supports_hotels": True,
            "supports_coordination": True,
            "input_modes": ["text"],
            "output_modes": ["text"],
            "skills": [
                "flight-search",
                "flight-booking", 
                "hotel-search",
                "hotel-booking"
            ]
        }