import main

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
    inputs = main.humanizeTokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(main.device)

    # Generate humanized output
    outputs = main.humanizeModel.generate(
        inputs,
        max_length=256,
        num_beams=5,
        num_return_sequences=1,
        temperature=1.5,
    )

    humanized_text = main.humanizeTokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "original_text": text,
        "humanized_text": humanized_text
    }
