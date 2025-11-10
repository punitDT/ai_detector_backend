from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

HUMANIZE_MODEL_NAME = "pszemraj/flan-t5-base-instruct-dolly_hhrlhf"

print("🔄 Loading Text Humanizer model...")

# Load model and tokenizer once globally
tokenizer = AutoTokenizer.from_pretrained(HUMANIZE_MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(HUMANIZE_MODEL_NAME)

# Move to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

print("✅ Humanizer model loaded successfully!")

async def humanize_text_service(text: str):
    """
    Paraphrases (humanizes) robotic or AI-sounding text to make it sound
    more natural and conversational.
    """
    text = text.strip()
    if not text:
        return {"error": "Empty text received"}

    # Prepare input for model
    input_text = f"paraphrase: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

    # Generate humanized output
    outputs = model.generate(
        inputs,
        max_length=256,
        num_beams=5,
        num_return_sequences=1,
        temperature=1.5,
    )

    humanized_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "original_text": text,
        "humanized_text": humanized_text
    }
