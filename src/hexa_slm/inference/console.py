import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
import torch
from hexa_slm.utils.model_loader import load_model_for_inference, get_streamer
import threading
import queue

app = typer.Typer()
console = Console()

@app.command()
def chat(
    model_path: str = typer.Option("models/cove_cybersec_lora", help="Path to the model or HuggingFace ID"),
    use_4bit: bool = typer.Option(True, help="Use 4-bit quantization"),
    system_prompt: str = typer.Option("You are a cybersecurity expert assistant.", help="System prompt for the chat"),
    cove: bool = typer.Option(False, "--cove", help="Enable Chain of Verification (CoVe) mode")
):
    """
    Start an interactive chat session with the HexaSLM model.
    """
    console.print(Panel.fit("[bold cyan]HexaSLM Interactive Chat[/bold cyan]", border_style="cyan"))
    
    if cove:
        console.print("[bold yellow]🧠 Chain of Verification (CoVe) Mode Enabled[/bold yellow]")
        system_prompt = "You are a cybersecurity expert. Verify all advice systematically."
    
    with console.status("[bold green]Loading model...[/bold green]", spinner="dots"):
        try:
            model, tokenizer = load_model_for_inference(model_path, use_4bit)
            console.print(f"[bold green]✔ Model loaded successfully from {model_path}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]✘ Failed to load model: {e}[/bold red]")
            # Fallback to base model if local path fails? Or just exit.
            # Let's try to be helpful
            if "models/cove_cybersec_lora" in model_path:
                 console.print("[yellow]Tip: Ensure you have the adapter in 'models/cove_cybersec_lora' or specify a valid path.[/yellow]")
            return

    # Chat loop
    console.print("[dim]Type 'exit', 'quit', or 'q' to end the session.[/dim]")
    
    # Alpaca style prompt format for instruction tuned models usually works well
    # or ChatML if the base model supports it. Qwen2.5 supports ChatML.
    # Let's use the tokenizer's chat template if available, otherwise fallback.
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # CoVe Assistant Starter
    cove_starter = "\nLet me provide thoroughly verified cybersecurity guidance.\n\n**Step 1 - Initial Analysis:**"

    while True:
        user_input = Prompt.ask("[bold blue]User[/bold blue]")
        
        if user_input.lower() in ["exit", "quit", "q"]:
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break
            
        messages.append({"role": "user", "content": user_input})
        
        # Format input
        try:
            # Apply chat template
            inputs_text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            
            # If CoVe is enabled, append the assistant's thought process starter
            if cove:
                inputs_text += cove_starter
                
            inputs = tokenizer(inputs_text, return_tensors="pt").to("cuda")
            
        except Exception as e:
             # Fallback if chat template issues
             text_prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant: "
             if cove:
                 text_prompt += cove_starter
             inputs = tokenizer(text_prompt, return_tensors="pt").to("cuda")

        # Streamer
        streamer = get_streamer(tokenizer)
        
        console.print("[bold magenta]Assistant:[/bold magenta]")
        # We can't easily capture the stream into a rich Live display while also printing to stdout with the basic TextStreamer.
        # For simplicity in this version, we will just let it print to stdout which unsloth/transformers streamer does.
        # To make it "rich", we'd need a custom streamer, but that might be overengineering for now.
        # Let's just run it.
        
        with torch.inference_mode():
             outputs = model.generate(
                inputs, 
                max_new_tokens=512, 
                streamer=streamer,
                use_cache=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Capture the output text (excluding input) to append to history
        # decode only the new tokens
        generated_ids = outputs[0][len(inputs[0]):]
        response_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        messages.append({"role": "assistant", "content": response_text})
        console.print() # Newline

if __name__ == "__main__":
    app()
