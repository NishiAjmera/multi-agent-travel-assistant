from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from agents import FlightsAgent
import os
from dotenv import load_dotenv

class FlightsAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        load_dotenv()
        openai_api_key =  os.getenv("OPENAI_API_KEY")
        self.agent = FlightsAgent(openai_api_key)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query=None
        for part in context._params.message.parts:
            if hasattr(part.root, 'text'):
                query = part.root.text
                break

        result = await self.agent.run(query)
        print(result)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')