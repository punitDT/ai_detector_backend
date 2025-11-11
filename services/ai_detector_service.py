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

def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    """
    Split text into chunks that fit within the model's token limit.
    Uses sentence boundaries to avoid splitting mid-sentence.

    Args:
        text: The text to chunk
        max_chars: Maximum characters per chunk (roughly 500 tokens)

    Returns:
        List of text chunks
    """
    # If text is short enough, return as-is
    if len(text) <= max_chars:
        return [text]

    # Split into sentences first
    sentences = simple_sentence_tokenize(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If a single sentence is too long, split it by words
        if len(sentence) > max_chars:
            # If we have accumulated text, save it first
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # Split long sentence into word-based chunks
            words = sentence.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 <= max_chars:
                    temp_chunk += word + " "
                else:
                    if temp_chunk:
                        chunks.append(temp_chunk.strip())
                    temp_chunk = word + " "
            if temp_chunk:
                chunks.append(temp_chunk.strip())

        # If adding this sentence would exceed limit, save current chunk
        elif len(current_chunk) + len(sentence) + 1 > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

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

    # Split text into chunks that fit within model's token limit
    chunks = chunk_text(text, max_chars=2000)

    # Analyze each chunk and collect scores
    chunk_scores = []
    chunk_labels = []

    for chunk in chunks:
        try:
            result = detector_client.text_classification(
                chunk,
                model=model,
            )[0]
            chunk_scores.append(float(result["score"]))
            chunk_labels.append(result["label"])
        except Exception as e:
            # If a chunk still fails, skip it
            print(f"Warning: Failed to analyze chunk: {str(e)}")
            continue

    # Calculate overall score as weighted average by chunk length
    if chunk_scores:
        overall_score = sum(chunk_scores) / len(chunk_scores)
        # Determine overall label based on majority vote
        fake_count = sum(1 for label in chunk_labels if label == "Fake")
        overall_label = "Fake" if fake_count > len(chunk_labels) / 2 else "Real"
    else:
        return {"error": "Failed to analyze text"}

    overall_score = round(overall_score, 4)

    # Analyze each sentence for detailed results
    sentences = simple_sentence_tokenize(text)
    detailed_results = []

    for sentence in sentences:
        # Skip very short sentences
        if len(sentence.strip()) < 10:
            continue

        try:
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
        except Exception as e:
            # If a sentence fails, skip it
            print(f"Warning: Failed to analyze sentence: {str(e)}")
            continue

    return {
        "overall": {
            "label": overall_label,
            "score": overall_score,
            "ai_likelihood": "High" if overall_score > 0.8 else "Medium" if overall_score > 0.5 else "Low"
        },
        "sentences": detailed_results,
        "chunks_analyzed": len(chunks)
    }
