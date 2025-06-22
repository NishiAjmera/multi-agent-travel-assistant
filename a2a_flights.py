from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

# =============================================================================
# FLIGHTS AGENT SKILLS AND CARD
# =============================================================================

flights_skill1 = AgentSkill(
    id='flight-search',
    name='Flight Search',
    description='Searches for available flights between cities on specific dates. Can filter by departure city, destination city, travel date, and provide pricing information.',
    tags=['flight-search', 'travel', 'booking', 'aviation']
)

flights_skill2 = AgentSkill(
    id='flight-booking',
    name='Flight Booking',
    description='Books flights for passengers after search. Handles passenger information, flight selection, and generates booking confirmations with reference numbers.',
    tags=['flight-booking', 'reservation', 'travel', 'confirmation']
)

flights_agent_card = AgentCard(
    name='Flight Booking Agent',
    description='AI agent specialized in flight search and booking services. Can help users find available flights between cities, compare prices, and complete flight bookings with confirmation details.',
    url='http://localhost:9999/agents/flights',
    version='1.0.0',
    defaultInputModes=['text'],
    defaultOutputModes=['text'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[flights_skill1, flights_skill2]
)
