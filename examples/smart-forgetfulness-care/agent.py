import os
import sys
import argparse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from rich.console import Console
from rich.panel import Panel

# DeepAgents Imports
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

# Local Imports
from skills.iot_tools import check_device_status, turn_off_device

# Load environment variables
load_dotenv()

console = Console()

def create_guardian_agent():
    """Create and return the Outing Guardian Deep Agent"""

    # Get base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Initialize Model from environment variables
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    api_base = os.getenv("OPENAI_API_BASE")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    model = ChatOpenAI(
        model=model_name,
        openai_api_base=api_base,
        openai_api_key=api_key,
        temperature=0
    )

    # Define Tools
    my_tools = [check_device_status, turn_off_device]

    # Create the Deep Agent
    agent = create_deep_agent(
        model=model,
        memory=[os.path.join(base_dir, "AGENTS.md")],  # Agent identity
        skills=[os.path.join(base_dir, "skills")],    # Skill directory
        tools=my_tools,                               # Tool functions
        subagents=[],
        backend=FilesystemBackend(root_dir=base_dir)
    )

    return agent


def main():
    """Main entry point for Outing Guardian CLI"""
    parser = argparse.ArgumentParser(
        description="Outing Guardian Agent: Remote Care for Forgetfulness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py "아 맞다, 고데기 끄고 나왔나?"
  python agent.py "침실 불 켰는지 확인 좀"
        """
    )
    parser.add_argument(
        "utterance",
        type=str,
        help="User's spoken utterance expressing anxiety about home devices"
    )

    args = parser.parse_args()

    # Display the user input
    console.print(Panel(
        f"[bold cyan]User:[/bold cyan] {args.utterance}",
        border_style="cyan"
    ))
    console.print()

    # Create the agent
    console.print("[dim]Initializing Outing Guardian...[/dim]")
    try:
        agent = create_guardian_agent()
    except Exception as e:
        console.print(f"[bold red]Failed to initialize agent:[/bold red] {e}")
        return

    # Invoke the agent
    console.print("[dim]Thinking & Acting...[/dim]\n")

    try:
        # Initialize Langfuse CallbackHandler
        langfuse_handler = CallbackHandler()

        # DeepAgents invoke format with callbacks
        result = agent.invoke(
            {"messages": [{"role": "user", "content": args.utterance}]},
            config={"callbacks": [langfuse_handler]}
        )

        # Extract and display the final answer
        # The result structure depends on the underlying agent executor, usually contains 'messages'
        final_message = result["messages"][-1]
        answer = final_message.content if hasattr(final_message, 'content') else str(final_message)

        console.print(Panel(
            f"[bold green]Guardian:[/bold green]\n\n{answer}",
            border_style="green"
        ))

    except Exception as e:
        console.print(Panel(
            f"[bold red]Error:[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == "__main__":
    main()
