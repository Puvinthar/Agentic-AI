"""
Agentic AI Logic using LangGraph
Implements intelligent routing and decision-making for the chatbot
"""
import os
import logging
from typing import TypedDict, Annotated, Sequence, Literal

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from datetime import datetime, timedelta
from dotenv import load_dotenv

from backend.tools import (
    get_weather_tool,
    query_document_tool,
    web_search_tool,
    query_meetings_tool,
    create_meeting_tool,
    load_document_tool
)

load_dotenv()
logger = logging.getLogger(__name__)


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """
    State that gets passed between nodes in the graph
    """
    messages: Sequence[BaseMessage]
    user_query: str
    intent: str
    tool_result: str
    final_response: str
    document_loaded: bool


# ============================================================================
# LLM INITIALIZATION
# ============================================================================

def get_llm():
    """
    Initialize LLM (Groq or OpenAI)
    Groq is recommended for its speed and free tier
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        logger.info("Using Groq LLM (llama-3.1-70b-versatile)")
        return ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.1-70b-versatile",
            temperature=0.3,
        )
    elif openai_api_key and openai_api_key != "your_openai_api_key_here":
        logger.info("Using OpenAI LLM (gpt-3.5-turbo)")
        return ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.3,
        )
    else:
        logger.warning("⚠️ No API key configured. Using mock responses.")
        return None


llm = get_llm()


# ============================================================================
# AGENT NODES
# ============================================================================

def intent_classifier(state: AgentState) -> AgentState:
    """
    Classify user intent to determine which agent/tool to use
    """
    user_query = state["user_query"].lower()
    
    # Intent classification logic
    if any(word in user_query for word in ["weather", "temperature", "sunny", "rainy", "climate"]):
        intent = "weather"
    elif any(word in user_query for word in ["meeting", "schedule", "calendar", "appointment"]):
        if any(word in user_query for word in ["create", "schedule", "add", "set up", "book"]):
            intent = "schedule_meeting"
        else:
            intent = "query_meeting"
    elif any(word in user_query for word in ["document", "pdf", "file", "upload"]):
        intent = "document_query"
    elif "?" in user_query or any(word in user_query for word in ["who", "what", "where", "when", "why", "how"]):
        # Check if document is loaded
        if state.get("document_loaded", False):
            intent = "document_query"
        else:
            intent = "general_search"
    else:
        intent = "general_search"
    
    logger.info(f"🎯 Intent classified: {intent}")
    state["intent"] = intent
    return state


def weather_agent(state: AgentState) -> AgentState:
    """
    Agent 1: Weather Intelligence Agent
    Handles weather-related queries
    """
    user_query = state["user_query"]
    
    # Extract location and time from query
    query_lower = user_query.lower()
    
    # Extract date
    date_query = "today"
    if "yesterday" in query_lower:
        date_query = "yesterday"
    elif "tomorrow" in query_lower:
        date_query = "tomorrow"
    
    # Extract location with better pattern matching
    location = None
    
    # Common cities with various spellings
    cities = [
        ("new york", "New York"),
        ("san francisco", "San Francisco"),
        ("los angeles", "Los Angeles"),
        ("bangalore", "Bangalore"),
        ("bengaluru", "Bangalore"),
        ("chennai", "Chennai"),
        ("mumbai", "Mumbai"),
        ("delhi", "Delhi"),
        ("new delhi", "New Delhi"),
        ("hyderabad", "Hyderabad"),
        ("kolkata", "Kolkata"),
        ("pune", "Pune"),
        ("london", "London"),
        ("paris", "Paris"),
        ("tokyo", "Tokyo"),
        ("singapore", "Singapore"),
        ("sydney", "Sydney"),
        ("dubai", "Dubai"),
        ("berlin", "Berlin"),
        ("toronto", "Toronto"),
    ]
    
    # Extract city from query - check for patterns like "in [city]" or "at [city]" or "[city] weather"
    for city_pattern, city_name in cities:
        if city_pattern in query_lower:
            location = city_name
            break
    
    # If no city found, return error message
    if not location:
        result = "⚠️ Please specify a city name. For example: 'What is the weather in London?' or 'Weather in Chennai today'"
    else:
        # Get weather
        result = get_weather_tool(location, date_query)
    
    state["tool_result"] = result
    
    logger.info(f"🌤️ Weather query executed for {location or 'no location'} ({date_query})")
    return state


def document_agent(state: AgentState) -> AgentState:
    """
    Agent 2: Document Understanding + Intelligent Section Extraction
    Handles document queries with smart section detection (skills, experience, etc.)
    """
    user_query = state["user_query"]
    
    # Query document with improved section-aware RAG
    doc_result = query_document_tool(user_query)
    
    # Only fall back to web search if explicitly about general knowledge, not document content
    query_lower = user_query.lower()
    is_document_specific = any(word in query_lower for word in ["skills", "experience", "education", "resume", "cv", "about", "summary", "projects", "work"])
    
    # Check if document doesn't have relevant answer AND it's not a document-specific query
    if not is_document_specific and any(phrase in doc_result for phrase in ["No document loaded", "does not contain relevant", "No relevant information"]):
        # Fallback to web search for general queries
        logger.info("📄 General query, using web search...")
        search_result = web_search_tool(user_query)
        
        if search_result and "❌" not in search_result and "⚠️" not in search_result:
            state["tool_result"] = f"📄 **Document Status:** No document loaded.\n\n{search_result}"
        else:
            state["tool_result"] = doc_result
    else:
        # Document has relevant answer or it's document-specific query - use it directly
        state["tool_result"] = doc_result
    
    logger.info("📄 Document query completed")
    return state


def meeting_scheduler_agent(state: AgentState) -> AgentState:
    """
    Agent 3: Meeting Scheduling + Weather Reasoning Agent
    Handles meeting creation with weather-based logic
    """
    user_query = state["user_query"]
    query_lower = user_query.lower()
    
    # Extract location for weather check
    location = None
    cities = [
        ("new york", "New York"), ("san francisco", "San Francisco"),
        ("bangalore", "Bangalore"), ("bengaluru", "Bangalore"),
        ("chennai", "Chennai"), ("mumbai", "Mumbai"),
        ("delhi", "Delhi"), ("hyderabad", "Hyderabad"),
        ("london", "London"), ("paris", "Paris"),
        ("tokyo", "Tokyo"), ("singapore", "Singapore")
    ]
    
    for city_pattern, city_name in cities:
        if city_pattern in query_lower:
            location = city_name
            break
    
    # If no location specified, ask user
    if not location:
        result = "⚠️ Please specify a city for the meeting. For example: 'Schedule a meeting in Chennai if weather is good'"
        state["tool_result"] = result
        return state
    
    # Determine date - default to tomorrow
    date_query = "tomorrow"
    meeting_date = datetime.now() + timedelta(days=1)
    meeting_date_str = meeting_date.strftime("%Y-%m-%d")
    
    if "today" in query_lower:
        date_query = "today"
        meeting_date = datetime.now()
        meeting_date_str = meeting_date.strftime("%Y-%m-%d")
    elif "tomorrow" in query_lower:
        date_query = "tomorrow"
    
    # Step 1: Check weather for the meeting date
    weather_result = get_weather_tool(location, date_query)
    
    # Step 2: Determine if weather is good
    is_good_weather = False
    weather_condition = "Unknown"
    
    if "clear" in weather_result.lower() or "sunny" in weather_result.lower():
        is_good_weather = True
        weather_condition = "Clear/Sunny ☀️"
    elif "cloud" in weather_result.lower() and "rain" not in weather_result.lower():
        is_good_weather = True
        weather_condition = "Partly Cloudy ☁️ (Acceptable)"
    elif "rain" in weather_result.lower() or "storm" in weather_result.lower():
        is_good_weather = False
        weather_condition = "Rainy/Stormy 🌧️ (Not Recommended)"
    else:
        is_good_weather = True
        weather_condition = "Moderate"
    
    # Step 3: Extract meeting title from query
    meeting_title = "Team Meeting"
    if "review" in query_lower:
        meeting_title = "Review Meeting"
    elif "standup" in query_lower:
        meeting_title = "Standup Meeting"
    elif "planning" in query_lower:
        meeting_title = "Planning Meeting"
    
    # Step 4: Decision logic based on weather
    if is_good_weather:
        # Create meeting with weather info
        create_result = create_meeting_tool(
            title=meeting_title,
            scheduled_date=meeting_date_str,
            location=location,
            description=f"Scheduled with weather consideration. Weather: {weather_condition}",
            weather_condition=weather_condition
        )
        
        result = f"""
{weather_result}

🤖 Weather Analysis: {weather_condition}
✅ Weather is suitable for a meeting!

{create_result}
        """
    else:
        result = f"""
{weather_result}

🤖 Weather Analysis: {weather_condition}
❌ Weather is not suitable for a meeting.
💡 Recommendation: Consider rescheduling or using virtual meeting.
        """
    
    state["tool_result"] = result.strip()
    logger.info("📅 Meeting scheduling logic executed")
    return state


def database_agent(state: AgentState) -> AgentState:
    """
    Agent 4: Natural Language → Database Query Agent
    Handles database queries using natural language
    """
    user_query = state["user_query"]
    
    # Query the database
    result = query_meetings_tool(user_query)
    state["tool_result"] = result
    
    logger.info("🗄️ Database query executed")
    return state


def general_search_agent(state: AgentState) -> AgentState:
    """
    General web search agent for queries that don't fit other categories
    """
    user_query = state["user_query"]
    
    result = web_search_tool(user_query)
    state["tool_result"] = result
    
    logger.info("🔍 Web search executed")
    return state


def response_generator(state: AgentState) -> AgentState:
    """
    Generate final response using LLM (if available) or direct tool result
    """
    tool_result = state.get("tool_result", "").strip()
    user_query = state["user_query"]
    
    if not tool_result:
        state["final_response"] = "Sorry, I couldn't generate a response. Please try again."
        return state
    
    if llm:
        try:
            # Use LLM to generate natural response
            system_message = """You are a professional AI assistant with expertise across multiple domains. 
Provide clear, accurate, and well-structured responses based strictly on the provided tool results.

Guidelines:
- Be professional yet approachable in tone
- Answer ONLY what was asked - avoid unnecessary elaboration
- For document queries: Extract and present the most relevant information concisely
- For weather queries: Format data clearly with key metrics highlighted
- For meetings: Present information in organized format
- Use bullet points or numbered lists when appropriate
- Never fabricate information not present in tool results
- If information is incomplete, acknowledge it professionally"""
            
            prompt = f"""User Query: {user_query}

Tool Results:
{tool_result}

Task: Generate a professional, focused response that directly answers the user's question. 
If the tool result contains a complete answer, you may use it with minor refinements for clarity and professionalism.
Ensure the response is concise and relevant to the specific question asked."""
            
            messages = [
                SystemMessage(content=system_message),
                HumanMessage(content=prompt)
            ]
            
            response = llm.invoke(messages)
            final_response = response.content.strip()
            
            if not final_response:
                final_response = tool_result
            
            state["final_response"] = final_response
            
        except Exception as e:
            logger.warning(f"LLM error: {e}, using tool result directly")
            state["final_response"] = tool_result
    else:
        # Use tool result directly if no LLM available
        state["final_response"] = tool_result
    
    logger.info("✅ Final response generated")
    return state


# ============================================================================
# GRAPH ROUTING
# ============================================================================

def route_intent(state: AgentState) -> str:
    """
    Route to appropriate agent based on intent
    """
    intent = state["intent"]
    
    routing_map = {
        "weather": "weather_agent",
        "document_query": "document_agent",
        "schedule_meeting": "meeting_scheduler_agent",
        "query_meeting": "database_agent",
        "general_search": "general_search_agent",
    }
    
    return routing_map.get(intent, "general_search_agent")


# ============================================================================
# BUILD GRAPH
# ============================================================================

def build_agent_graph():
    """
    Build the LangGraph workflow
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("intent_classifier", intent_classifier)
    workflow.add_node("weather_agent", weather_agent)
    workflow.add_node("document_agent", document_agent)
    workflow.add_node("meeting_scheduler_agent", meeting_scheduler_agent)
    workflow.add_node("database_agent", database_agent)
    workflow.add_node("general_search_agent", general_search_agent)
    workflow.add_node("response_generator", response_generator)
    
    # Set entry point
    workflow.set_entry_point("intent_classifier")
    
    # Add conditional routing
    workflow.add_conditional_edges(
        "intent_classifier",
        route_intent,
        {
            "weather_agent": "weather_agent",
            "document_agent": "document_agent",
            "meeting_scheduler_agent": "meeting_scheduler_agent",
            "database_agent": "database_agent",
            "general_search_agent": "general_search_agent",
        }
    )
    
    # All agents lead to response generator
    workflow.add_edge("weather_agent", "response_generator")
    workflow.add_edge("document_agent", "response_generator")
    workflow.add_edge("meeting_scheduler_agent", "response_generator")
    workflow.add_edge("database_agent", "response_generator")
    workflow.add_edge("general_search_agent", "response_generator")
    
    # Response generator is the end
    workflow.add_edge("response_generator", END)
    
    return workflow.compile()


# Initialize the graph
agent_graph = build_agent_graph()


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def process_query_sync(user_query: str, document_loaded: bool = False) -> str:
    """
    Process user query through the agentic workflow (SYNCHRONOUS VERSION)
    
    Args:
        user_query: User's question or command
        document_loaded: Whether a document is currently loaded
    
    Returns:
        Final response from the agent
    """
    try:
        if not user_query or not user_query.strip():
            return "❌ Please provide a valid query."
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=user_query)],
            "user_query": user_query.strip(),
            "intent": "",
            "tool_result": "",
            "final_response": "",
            "document_loaded": document_loaded,
        }
        
        # Run the graph (synchronous)
        logger.info(f"🚀 Processing query: {user_query}")
        result = agent_graph.invoke(initial_state)
        
        final_response = result.get("final_response", "").strip()
        
        if not final_response:
            final_response = "Sorry, I couldn't generate a response. Please try again."
        
        return final_response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return f"❌ Error processing your request: {str(e)}"


async def process_query(user_query: str, document_loaded: bool = False) -> str:
    """
    Process user query through the agentic workflow (ASYNC WRAPPER)
    
    Args:
        user_query: User's question or command
        document_loaded: Whether a document is currently loaded
    
    Returns:
        Final response from the agent
    """
    import asyncio
    return await asyncio.to_thread(
        process_query_sync, user_query, document_loaded
    )
