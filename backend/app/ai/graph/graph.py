from langgraph.graph import StateGraph, END
from app.ai.graph.state import AIState
from app.ai.graph.nodes import extract_node, plan_node, reminder_node, recover_node, chat_node
from app.ai.graph.router import route_action

def build_graph():
    workflow = StateGraph(AIState)

    # Add nodes
    workflow.add_node("extract_node", extract_node)
    workflow.add_node("plan_node", plan_node)
    workflow.add_node("reminder_node", reminder_node)
    workflow.add_node("recover_node", recover_node)
    workflow.add_node("chat_node", chat_node)

    # Add conditional routing from a "start" abstraction
    # LangGraph requires an entry point. We can use a dummy start node that just routes.
    workflow.set_conditional_entry_point(
        route_action,
        {
            "extract_node": "extract_node",
            "plan_node": "plan_node",
            "reminder_node": "reminder_node",
            "recover_node": "recover_node",
            "chat_node": "chat_node"
        }
    )

    # Route all nodes to END
    workflow.add_edge("extract_node", END)
    workflow.add_edge("plan_node", END)
    workflow.add_edge("reminder_node", END)
    workflow.add_edge("recover_node", END)
    workflow.add_edge("chat_node", END)

    return workflow.compile()

ai_graph = build_graph()
