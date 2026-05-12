from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.exa import ExaTools

agent = Agent(
    name="Shelfie",
    description="Book recommendation assistant",

    model=Groq(
        id="openai/gpt-oss-120b",
        max_tokens=800   # ✅ controls response size
    ),

    instructions=[
        "Recommend books based on user preferences.",
        "Suggest up to 5 books.",
        "Include short summaries.",
        "Mix modern and popular titles.",
        "Be concise."
    ],

    tools=[
        ExaTools(num_results=3)  # ✅ reduce tool output
    ],

    max_history=2,              # ✅ prevents memory explosion
    show_tool_calls=False       # ✅ avoids extra tokens
)

agent.print_response(
    "Books like Anxious People and Lessons in Chemistry"
)