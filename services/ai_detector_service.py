from nltk.tokenize import sent_tokenize
import main

async def detect_text_service(text: str):
    """
    Detect AI-generated text using HuggingFace Inference API
    """
    text = text.strip()
    if not text:
        return {"error": "Empty text received"}

    # Use HuggingFace Inference API for text classification
    global_result = main.detector_client.text_classification(
        text,
        model=main.DETECTOR_MODEL,
    )[0]

    overall_label = global_result["label"]
    overall_score = round(float(global_result["score"]), 4)

    # Analyze each sentence
    sentences = sent_tokenize(text)
    detailed_results = []

    for sentence in sentences:
        result = main.detector_client.text_classification(
            sentence,
            model=main.DETECTOR_MODEL,
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
