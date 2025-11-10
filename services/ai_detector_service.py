from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from nltk.tokenize import sent_tokenize
import nltk

# Ensure tokenizers are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt", quiet=True)

MODEL_NAME = "openai-community/roberta-base-openai-detector"
HUMANIZE_MODEL_NAME = "rVamsi/T5_Paraphrase_Paws"
print("🔄 Loading AI detector model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
detector = pipeline("text-classification", model=model, tokenizer=tokenizer, truncation=True)

print("✅ Model loaded successfully!")

async def detect_text_service(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text received"}

    global_result = detector(text)[0]
    overall_label = global_result["label"]
    overall_score = round(float(global_result["score"]), 4)

    sentences = sent_tokenize(text)
    detailed_results = []

    for sentence in sentences:
        result = detector(sentence)[0]
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
