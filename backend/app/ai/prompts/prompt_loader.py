import os

PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def load_prompt(name: str) -> str:
    """Loads a prompt template from a markdown file in the prompts directory."""
    path = os.path.join(PROMPTS_DIR, f"{name}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()
