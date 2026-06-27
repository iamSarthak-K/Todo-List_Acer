from app.ai.graph.state import AIState
from app.ai.agents.commitment_agent import CommitmentAgent
from app.ai.agents.planner_agent import PlannerAgent
from app.ai.agents.reminder_agent import ReminderAgent
from app.ai.agents.recovery_agent import RecoveryAgent
from app.ai.agents.chat_agent import ChatAgent

def extract_node(state: AIState) -> AIState:
    agent = CommitmentAgent()
    state["response"] = agent.execute(state)
    return state

def plan_node(state: AIState) -> AIState:
    agent = PlannerAgent()
    state["response"] = agent.execute(state)
    return state

def reminder_node(state: AIState) -> AIState:
    agent = ReminderAgent()
    state["response"] = agent.execute(state)
    return state

def recover_node(state: AIState) -> AIState:
    agent = RecoveryAgent()
    state["response"] = agent.execute(state)
    return state

def chat_node(state: AIState) -> AIState:
    agent = ChatAgent()
    state["response"] = agent.execute(state)
    return state
