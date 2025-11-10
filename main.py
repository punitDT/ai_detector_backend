from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from nltk.tokenize import sent_tokenize
import nltk
import torch

# Download the sentence tokenizer if not already present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt/PY3/punkt.tab.pickle')
except LookupError:
    # Ensure required tokenizers are downloaded
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)


# Initialize FastAPI app
app = FastAPI(title="AI Text Detector API", version="2.0")

# Define input model
class TextInput(BaseModel):
    text: str

# Load model once at startup (this avoids reloading on every request)
MODEL_NAME = "openai-community/roberta-base-openai-detector"
print("🔄 Loading AI detector model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
detector = pipeline("text-classification", model=model, tokenizer=tokenizer)

print("✅ Model loaded successfully!")

@app.post("/detect")
async def detect_text(input: TextInput):
    text = input.text.strip()

    if not text:
        return {"error": "Empty text received"}

    # -------- 1️⃣ GLOBAL DETECTION --------
    global_result = detector(text)[0]
    overall_label = global_result["label"]
    overall_score = round(float(global_result["score"]), 4)

    # Convert label to more interpretable terms
    overall_is_ai = True if "AI" in overall_label or "Fake" in overall_label else False

    # -------- 2️⃣ SENTENCE-LEVEL DETECTION --------
    sentences = sent_tokenize(text)
    detailed_results = []

    for sentence in sentences:
        try:
            result = detector(sentence)[0]
            detailed_results.append({
                "sentence": sentence,
                "label": result["label"],
                "score": round(float(result["score"]), 4),
                "ai_likelihood": "High" if result["score"] > 0.8 else "Medium" if result["score"] > 0.5 else "Low"
            })
        except Exception as e:
            detailed_results.append({
                "sentence": sentence,
                "error": str(e)
            })

    # -------- 🧩 COMBINE RESULTS --------
    response = {
        "overall": {
            "label": overall_label,
            "score": overall_score,
            "ai_likelihood": "High" if overall_score > 0.8 else "Medium" if overall_score > 0.5 else "Low"
        },
        "sentences": detailed_results
    }

    return response
