import uuid
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from InquirerPy import inquirer
import db_agent.config as local_config
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from .agents import ReactiveAgent
from .utils import create_conn_url,reserved_words
import asyncio
import warnings
import os
from db_agent.utils.constants import AVAILABLE_MODEL_PROVIDERS

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" 

console = Console()
thread_id = uuid.uuid4()

def display_header():
    console.print(Panel.fit(
        Text("My CLI Configuration Tool", style="bold cyan"),
        title="Welcome",
        border_style="bright_magenta"
    ))


def reset_session():
    global thread_id
    thread_id = uuid.uuid4()

def handle_reserved_word(word):
    """Handle the reserved word based on its action."""
    if word == "exit":
        console.print("[bold red]Exiting the chat. Goodbye![/bold red]")
        return False
    elif word == "help":
        console.print("[bold cyan]Available commands:[/bold cyan] exit, help, clear, reset")
    elif word == "clear":
        console.clear()
        console.print("[bold green]Chat cleared![/bold green]")
    elif word == "reset":
        reset_session()
        console.print("[bold yellow]Session reset![/bold yellow]")
    return True



def save_api_key():
    api_key = inquirer.text(
        message="🔑 Enter your API key:",
        validate=lambda x: len(x) > 0 or "API key cannot be empty."
    ).execute()
    local_config.save_api_key(api_key)
    console.print("[green]✔ API key saved successfully![/green]")

def save_db_info():
    host = inquirer.text(
        message="🌐 Database Host:",
        default="localhost"
    ).execute()
    user = inquirer.text(
        message="👤 Database User:"
    ).execute()
    password = inquirer.secret(
        message="🔑 Database Password:"
    ).execute()
    database = inquirer.text(
        message="💾 Database Name:"
    ).execute()
    port = inquirer.number(
        message="🔢 Database Port:",
        default=5432
    ).execute()

    local_config.save_db_info(host, user, password, database, port)
    console.print("[green]✔ Database information saved successfully![/green]")

def show_config():
    config = local_config.load_config()
    if config:
        panel_content = ""
        for key, value in config.items():
            if key == "db_info":
                db_details = "\n".join([f"{k}: {v}" for k, v in value.items()])
                panel_content += f"[bold yellow]Database Information:[/bold yellow]\n{db_details}\n"
            else:
                panel_content += f"[bold yellow]{key}:[/bold yellow] {value}\n"
        console.print(Panel(panel_content, title="Stored Configuration", border_style="bright_green"))
    else:
        console.print("[red]⚠ No configuration found. Please set up your API key and database info.[/red]")

def show_available_commands():
    """Display available commands."""
    console.print("\n[bold cyan]Available Commands:[/bold cyan]")
    for command, description in reserved_words.items():
        console.print(f"  [bold green]{command}[/bold green] - {description}")
    console.print("")




def chat():
    show_available_commands()
    
    while True:
        prompt = Prompt.ask("Enter your question:")
        if not prompt:
            console.print("[red]⚠ Please enter your question.[/red]")
            continue
        if prompt.lower() in reserved_words:
            if not handle_reserved_word(prompt.lower()):
                break
            continue
        
        # Get model info and database connection URL
        [provider_name, model] = local_config.get_model_info()
        db_conn_url = create_conn_url(local_config.get_db_info())
        agent = ReactiveAgent(provider_name, model, db_conn_url)

        # Use a spinner to indicate thinking
        with Live(Spinner("dots", text="Thinking..."), refresh_per_second=8):
            # Run the async function
            response = asyncio.run(agent._run_async(prompt, str(thread_id)))
        
        # Display the response
        console.print(f"[bold yellow]🤖 Chatbot:[/bold yellow] {response.content}")


def save_model_config():
    choice = inquirer.select(
            message="Please select the available LLM providers:",
            choices= AVAILABLE_MODEL_PROVIDERS + ["Exit"],
            default="google"
        ).execute()
    if choice == "Exit":
        console.print("[red]✖ Operation cancelled by the user.[/red]")
        return
    provider_name = inquirer.text(
        message="Enter the name of your model:"
    ).execute()
    local_config.save_model_config(choice, provider_name)
    console.print("[green]✔ Model configuration  saved successfully![/green]")

async def display_thinking():
    """Displays a thinking spinner asynchronously."""
    with Live(Spinner("dots", text="🤔 Thinking...", style="bold blue"), refresh_per_second=10):
        while True:
            await asyncio.sleep(0.1)  # Refresh rate

def main():
    display_header()
    choice = inquirer.select(
        message="Please select an option:",
        choices=[
            "Save API Key",
            "Save Database Info",
            "Show Configuration",
            "Configure LLM",
            "Chat",
            "Exit"
        ],
        default="Chat"
    ).execute()

    if choice == "Save API Key":
        save_api_key()
    elif choice == "Save Database Info":
        save_db_info()
    elif choice == "Show Configuration":
        show_config()
    elif choice == "Configure LLM":
        save_model_config()  
    elif choice == "Chat":
        chat()
    elif choice == "Exit":
        console.print("[bold blue]Goodbye![/bold blue]")
        return

    main()

if __name__ == "__main__":
    main()
