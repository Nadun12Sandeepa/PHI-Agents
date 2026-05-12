from phi.agent import Agent 
from phi.model.groq import Groq

agent=Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    description="You are a famous short writer asked to write  for a magazine",
    instructions=["you are a pilot on a plane flying from Hawai to Japan "],
    markdown=True,
    debug_mode=True,
)

agent.print_response("Tell me a 2 sentence horror story",stream=True)
