import torch
from unsloth import FastLanguageModel
from transformers import TextStreamer

def load_model_for_inference(model_path: str, load_in_4bit: bool = True):
    """
    Loads a model for inference using Unsloth.

    Args:
        model_path (str): Path to the model or HuggingFace repo ID.
        load_in_4bit (bool): Whether to load in 4-bit quantization.

    Returns:
        model, tokenizer
    """
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_path,
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=load_in_4bit,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer

def get_streamer(tokenizer):
    """Returns a TextStreamer for streaming output."""
    return TextStreamer(tokenizer)
