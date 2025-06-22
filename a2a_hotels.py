from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
# =============================================================================
# HOTELS AGENT SKILLS AND CARD
# =============================================================================

hotels_skill1 = AgentSkill(
    id='hotel-search',
    name='Hotel Search',
    description='Searches for available hotels in cities based on check-in/check-out dates. Provides hotel options with pricing, amenities, and location information.',
    tags=['hotel-search', 'accommodation', 'travel', 'lodging']
)

hotels_skill2 = AgentSkill(
    id='hotel-booking',
    name='Hotel Booking',
    description='Books hotel reservations for guests. Manages guest information, room selection, date preferences, and generates booking confirmations with reference numbers.',
    tags=['hotel-booking', 'reservation', 'accommodation', 'confirmation']
)

hotels_agent_card = AgentCard(
    name='Hotel Booking Agent',
    description='AI agent specialized in hotel search and booking services. Can help users find available accommodations in various cities, compare rates, and complete hotel reservations with confirmation details.',
    url='http://localhost:9999/agents/hotels',
    version='1.0.0',
    defaultInputModes=['text'],
    defaultOutputModes=['text'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[hotels_skill1, hotels_skill2]
)
