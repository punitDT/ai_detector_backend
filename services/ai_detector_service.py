import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from huggingface_hub import InferenceClient

def simple_sentence_tokenize(text: str) -> list[str]:
    """
    Simple sentence tokenizer that splits on common sentence boundaries.
    Works without external dependencies and handles most common cases.
    """
    # Split on sentence-ending punctuation followed by whitespace and capital letter
    # This regex handles: . ! ? followed by space and capital letter
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)

    # Filter out empty strings and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences

async def detect_text_service(text: str, detector_client: "InferenceClient" = None, model: str = None):
    """
    Detect AI-generated text using HuggingFace Inference API

    Args:
        text: The text to analyze
        detector_client: HuggingFace InferenceClient instance
        model: Model name to use for detection
    """
    # Import here to avoid circular dependency
    if detector_client is None or model is None:
        import main
        detector_client = main.detector_client
        model = main.DETECTOR_MODEL

    text = text.strip()
    if not text:
        return {"error": "Empty text received"}

    # Use HuggingFace Inference API for text classification
    global_result = detector_client.text_classification(
        text,
        model=model,
    )[0]

    overall_label = global_result["label"]
    overall_score = round(float(global_result["score"]), 4)

    # Analyze each sentence
    sentences = simple_sentence_tokenize(text)
    detailed_results = []

    for sentence in sentences:
        result = detector_client.text_classification(
            sentence,
            model=model,
        )[0]

        detailed_results.append({
            "sentence": sentence,
            "label": result["label"],
            "score": round(float(result["score"]), 4),
            "ai_likelihood": "High" if result["score"] > 0.8 else "Medium" if result["score"] > 0.5 else "Low"
        })

    return {
        "overall": {
            "label": overall_label,
            "score": overall_score,
            "ai_likelihood": "High" if overall_score > 0.8 else "Medium" if overall_score > 0.5 else "Low"
        },
        "sentences": detailed_results
    }
