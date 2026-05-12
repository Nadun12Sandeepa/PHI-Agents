from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

# 🌐 Web Agent (ONLY for news/search)
web_agent = Agent(
    name="Web Agent",
    role="Search and return latest news",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=[
        "Search the web for latest news",
        "Always include sources",
        "Do not do financial analysis"
    ],
    show_tool_calls=True,
    markdown=True,
)

# 📊 Finance Agent (NO tools)
finance_agent = Agent(
    name="Finance Agent",
    role="Analyze stock recommendations",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Summarize analyst recommendations clearly",
        "Use tables",
        "Do not call any tools"
    ],
    show_tool_calls=True,
    markdown=True,
)

# 🤖 Team Agent
agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    instructions=[
        "For news, use Web Agent",
        "For analyst recommendations, use Finance Agent",
        "Combine both into a final answer"
    ],
    show_tool_calls=True,
    markdown=True,
)

# 🚀 Run (NO STREAMING first)
agent_team.print_response(
    "Summarize analyst recommendations and latest news for NVIDIA (NVDA)",
    stream=False
)

'''
Great — this is exactly how you should study agent systems 👍
I’ll go **line by line**, and for each part explain:

* ✅ *What it does*
* 🎯 *Why it’s used*
* ⚠️ *What could go wrong / alternatives*

---

# 🔹 IMPORTS

```python
from phi.agent import Agent
```

✅ **What:** Imports the `Agent` class
🎯 **Why:** This is the core building block — every AI agent (web, finance, team) is created using this
⚠️ Without this → you cannot create agents

---

```python
from phi.model.groq import Groq
```

✅ **What:** Imports Groq model wrapper
🎯 **Why:** Lets your agent use Groq-hosted LLMs (fast inference)
⚠️ If model name is wrong → 💥 API error (you already saw this)

---

```python
from phi.tools.duckduckgo import DuckDuckGo
```

✅ **What:** Imports a search tool
🎯 **Why:** Allows agent to fetch **real-time web data**
⚠️ Without tools → agent only uses its training knowledge (no latest news)

---

# 🌐 WEB AGENT (NEWS SPECIALIST)

```python
web_agent = Agent(
```

✅ **What:** Creating a new agent instance
🎯 **Why:** This agent will handle **web search tasks**

---

```python
    name="Web Agent",
```

✅ **What:** Name of the agent
🎯 **Why:** Helps team agent identify it
⚠️ Important in multi-agent setups (used internally for routing)

---

```python
    role="Search and return latest news",
```

✅ **What:** Defines responsibility
🎯 **Why:** Helps LLM decide:

> “This agent = news tasks”

⚠️ If roles overlap → agents get confused (you had this issue earlier)

---

```python
    model=Groq(id="openai/gpt-oss-20b"),
```

✅ **What:** Assigns LLM
🎯 **Why:** This is the “brain” of the agent

⚠️ Notes:

* Must be **valid Groq model**
* Different models = different performance

---

```python
    tools=[DuckDuckGo()],
```

✅ **What:** Adds tool(s)
🎯 **Why:** Enables:

* searching web
* getting latest info

⚠️ Without this → no real-time news

---

```python
    instructions=[
        "Search the web for latest news",
        "Always include sources",
        "Do not do financial analysis"
    ],
```

✅ **What:** Behavior rules
🎯 **Why:** Controls how the agent behaves

Example:

* Forces **source citation**
* Prevents overlap with finance agent

⚠️ Very important in multi-agent systems

---

```python
    show_tool_calls=True,
```

✅ **What:** Debug feature
🎯 **Why:** Shows when agent calls a tool

Example output:

```
Calling DuckDuckGo...
```

⚠️ Turn off in production

---

```python
    markdown=True,
```

✅ **What:** Format output
🎯 **Why:** Makes response structured (tables, bullets)

---

# 📊 FINANCE AGENT

```python
finance_agent = Agent(
```

✅ Creates second agent

---

```python
    name="Finance Agent",
    role="Analyze stock recommendations",
```

🎯 This agent handles:

* analyst ratings
* stock insights

---

```python
    model=Groq(id="openai/gpt-oss-20b"),
```

Same model, different role

---

```python
    instructions=[
        "Summarize analyst recommendations clearly",
        "Use tables",
        "Do not call any tools"
    ],
```

✅ Key design choice

🎯 Why no tools?

* Prevents bad tool calls (your earlier error)
* Keeps it **reasoning-only**

⚠️ If you add tools → risk of function-call errors again

---

# 🤖 TEAM AGENT (MAIN CONTROLLER)

```python
agent_team = Agent(
```

✅ This is the **boss agent**

---

```python
    model=Groq(id="openai/gpt-oss-20b"),
```

🎯 This model decides:

* which agent to use
* how to combine results

---

```python
    team=[web_agent, finance_agent],
```

✅ Defines sub-agents

🎯 Enables:

* delegation
* task splitting

---

```python
    instructions=[
        "For news, use Web Agent",
        "For analyst recommendations, use Finance Agent",
        "Combine both into a final answer"
    ],
```

✅ VERY IMPORTANT

🎯 This controls:

* routing logic
* final output structure

Without this → chaos 😅

---

```python
    show_tool_calls=True,
    markdown=True,
```

Same purpose as before:

* debug + formatting

---

# 🚀 EXECUTION

```python
agent_team.print_response(
```

✅ Runs the system

---

```python
    "Summarize analyst recommendations and latest news for NVIDIA (NVDA)",
```

🎯 User query

What happens internally:

1. Team agent reads query
2. Splits task:

   * Finance → recommendations
   * Web → news
3. Calls each agent
4. Combines results

---

```python
    stream=False
)
```

✅ Execution mode

🎯 Why `False`:

* safer
* avoids streaming + tool bugs

---

# 🔄 FULL FLOW (IMPORTANT)

Your system works like this:

```
User Query
   ↓
Team Agent
   ↓
 ┌───────────────┬───────────────┐
 ↓               ↓
Web Agent     Finance Agent
(search)      (analyze)
 ↓               ↓
   ← Combine results →
         ↓
     Final Output
```

---

# ⚠️ Key Design Decisions You Did RIGHT

✔ Separated roles
✔ Avoided tools in finance agent
✔ Added instructions for routing
✔ Disabled streaming

👉 This is actually a **good architecture**

---

# 🚨 Potential Improvements

### 1. Better model

```python
Groq(id="llama-3.3-70b-versatile")
```

👉 More stable than `gpt-oss-20b`

---

### 2. Add real finance data (BIG upgrade)

Instead of:

```python
DuckDuckGo()
```

Use:

* Yahoo Finance API
* Alpha Vantage

👉 Gives real analyst ratings

---

### 3. Add fallback behavior

```python
"If unsure, respond without calling tools"
```

👉 Prevents crashes

---

# 🧠 Simple Analogy

Think of your system like a company:

| Component     | Role              |
| ------------- | ----------------- |
| Team Agent    | Manager           |
| Web Agent     | News reporter     |
| Finance Agent | Financial analyst |
| DuckDuckGo    | Internet          |


'''