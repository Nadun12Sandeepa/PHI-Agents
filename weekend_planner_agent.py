from phi.agent import Agent 
from phi.model.groq import Groq 
from phi.tools.exa import ExaTools


agent=Agent(
    description="You help the user plan their weekends",
    name="Timeout",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "You are a weekend planning assistant.",
        "Provide sections: Events, Activities, Dining.",
        "Ensure recommendations match the given dates and location.",
        "Keep responses concise and relevant.",
        "Use external tools sparingly and summarize results briefly.",
    ],
    tools=[ExaTools(num_results=2,text_length_limit=500)]
)

agent.print_response(
    "I want to plan my coming weekend filled with fun actvities and christmas themed activities in Bangalore for 21 and 22 Dec 2024."
)