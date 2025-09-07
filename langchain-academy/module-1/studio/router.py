from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# LLM with bound tool
llm =  ChatOllama(model="llama3.2:1b")
llm_with_tools = llm.bind_tools([multiply])

# Node
# This node is used for checking if the tool should be invoked. The bind_tools is probably doing
# some magic in the background. This calls the LLM to check if the tool should be invoked or not.
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
# This node makes a decision whether the tool will be called or not.
builder.add_node("tool_calling_llm", tool_calling_llm)

# This node is the actual tool call.
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)

# Compile graph
graph = builder.compile()