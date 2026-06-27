from app.ai.graph.state import AIState

def route_action(state: AIState) -> str:
    """Routes the state to the appropriate agent node based on the action."""
    action = state.get("action")
    if action == "extract":
        return "extract_node"
    elif action == "plan":
        return "plan_node"
    elif action == "reminder":
        return "reminder_node"
    elif action == "recover":
        return "recover_node"
    elif action == "chat":
        return "chat_node"
    else:
        raise ValueError(f"Unknown action: {action}")
