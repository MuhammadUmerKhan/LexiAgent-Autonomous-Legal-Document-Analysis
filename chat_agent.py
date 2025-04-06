import logging, json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import ToolMessage
from langchain.tools import Tool
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from clause_extractor import get_clause_extracted
from classify_documents import get_classified_doc
from risk_detector import get_clause_risks
from summarizer import get_doc_summary
from utils.utils import configure_llm

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/langgraph.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Chatbot Agent and Tools ---

# Define Chatbot State Schema
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
    file_path: str

# Chatbot Tools
tools = [
    Tool(
        name="ClassifyDocument",
        func=lambda file_path: get_classified_doc(file_path),
        description="Classify the uploaded legal document as a specific type."
    ),
    Tool(
        name="ExtractClauses",
        func=lambda file_path: get_clause_extracted(file_path),
        description="Extract clauses from the uploaded legal document."
    ),
    Tool(
        name="DetectRisks",
        func=lambda file_path: get_clause_risks(file_path),
        description="Detect risks in the uploaded legal document."
    ),
    Tool(
        name="SummarizeDocument",
        func=lambda file_path: get_doc_summary(file_path),
        description="Summarize the uploaded legal document."
    ),
]

# Define Tool Executor Class
class ToolExecutor:
    def __init__(self, tools: list):
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def __call__(self, state: ChatState):
        messages = state.get("messages", [])
        last_message = messages[-1] if messages else None
        
        if not last_message or not hasattr(last_message, "tool_calls"):
            return {"messages": messages}
        
        tool_results = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            file_path = state["file_path"]  # Pass file_path from state
            
            if tool_name in self.tools_by_name:
                tool_result = self.tools_by_name[tool_name].invoke(file_path)
                tool_results.append(ToolMessage(
                    content=json.dumps(tool_result),
                    tool=tool_name,
                    tool_call_id=tool_call["id"]
                ))
        
        return {"messages": messages + tool_results}

# Define Routing Function
def route_tools(state: ChatState):
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return END

# Build Chatbot Graph
graph_builder = StateGraph(ChatState)
llm = configure_llm(MODEL_NAME="meta-llama/llama-4-scout-17b-16e-instruct")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: ChatState):
    """Handles AI response and tool calling."""
    ai_response = llm_with_tools.invoke(state["messages"])
    return {"messages": [ai_response]}

# Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolExecutor(tools))
graph_builder.add_conditional_edges("chatbot", route_tools, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile the graph
chat_graph = graph_builder.compile()

def stream_chat_response(user_input: str, file_path: str) -> str:
    """Streams chatbot responses and formats them for legal document analysis."""
    messages = [
        {"role": "system", "content": (
            "You are LexiAgent, a professional AI-powered legal document assistant. "
            "Always respond in a clear, concise, and professional tone. "
            "Format responses with headings and bullet points for readability. "
            "Use polite language and helpful suggestions. "
            "Enhance responses with **appropriate emojis** like 📄 for documents, ⚠️ for risks, and ✅ for confirmations. "
            "Maintain a formal yet approachable style in every response. "
            "Always respond in English."
        )}
    ]
    messages.append({"role": "user", "content": user_input})

    final_response = ""
    for event in chat_graph.stream({"messages": messages, "file_path": file_path}):
        for value in event.values():
            assistant_message = value["messages"][-1]
            if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
                continue  # Skip intermediate tool call messages
            content = assistant_message.content
            if isinstance(assistant_message, ToolMessage):
                tool_result = json.loads(content)
                if assistant_message.tool == "ClassifyDocument":
                    final_response += "### 📄 Document Type\n"
                    final_response += f"- {tool_result}\n"
                elif assistant_message.tool == "ExtractClauses":
                    final_response += "### 📌 Found Clauses\n"
                    for clause, detail in tool_result.items():
                        final_response += f"- **{clause}**: {detail}\n"
                elif assistant_message.tool == "DetectRisks":
                    final_response += "### ⚠️ Risks\n#### Ambiguous Clauses\n"
                    for clause, issue in tool_result["ambiguous_clauses"].items():
                        final_response += f"- **{clause}**: {issue}\n"
                    final_response += "#### Suggestions\n"
                    for clause, suggestion in tool_result["suggestions"].items():
                        final_response += f"- **{clause}**: {suggestion}\n"
                elif assistant_message.tool == "SummarizeDocument":
                    final_response += "### 📝 Summary\n"
                    bullets = [line.strip() for line in tool_result.split("\n") if line.strip().startswith("-")]
                    for bullet in bullets:
                        final_response += f"{bullet}\n"
            else:
                final_response += content + "\n"
    
    return final_response.strip()