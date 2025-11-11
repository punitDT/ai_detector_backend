# AI Text Detector API

A FastAPI-based backend service for detecting AI-generated text and humanizing content using HuggingFace models.

## Features

- 🔍 **AI Text Detection**: Detect AI-generated content using RoBERTa model
- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🤖 **Text Humanization**: Placeholder for text humanization (coming soon)
- 🚀 **Fast & Lightweight**: Optimized for free-tier deployments

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai_detector_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your HuggingFace token
```

5. **Run the server**
```bash
python main.py
# Or use uvicorn directly:
# uvicorn main:app --reload --port 8000
```

6. **Test the API**
- Health check: http://localhost:8000/
- API docs: http://localhost:8000/docs

## API Endpoints

### Health Check
- `GET /` - API status and available endpoints
- `GET /health` - Simple health check

### Detection
- `POST /api/detect` - Detect AI-generated text
  ```json
  {
    "text": "Your text here"
  }
  ```

### Upload
- `POST /api/upload` - Upload and analyze documents (PDF, DOCX, TXT)

### Humanize
- `POST /api/humanize` - Humanize text (placeholder)

## Deployment on Render (Free Tier)

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Set Environment Variables**
   - Go to Environment tab
   - Add `HF_TOKEN` with your HuggingFace API token

4. **Deploy**
   - Render will automatically deploy using the configuration in `render.yaml`

### Option 2: Manual Configuration

1. **Create a new Web Service on Render**

2. **Configure Build & Deploy**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `HF_TOKEN`: Your HuggingFace API token
   - `PYTHON_VERSION`: 3.11.0 (optional)

4. **Deploy**

### Important Notes for Free Tier

- ✅ The app uses HuggingFace Inference API (no local model loading)
- ✅ Lightweight dependencies optimized for free tier
- ✅ Health check endpoint at `/` for Render's monitoring
- ⚠️ Free tier services spin down after 15 minutes of inactivity
- ⚠️ First request after spin-down may take 30-60 seconds

### Testing Your Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.onrender.com/

# Test detection
curl -X POST https://your-app.onrender.com/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test sentence."}'
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HF_TOKEN` | Yes | HuggingFace API token for model inference |
| `PORT` | No | Server port (default: 8000, Render sets this automatically) |

## Models Used

- **Detector**: `openai-community/roberta-base-openai-detector`
- **Humanizer**: `google/flan-t5-base` (placeholder, not currently active)

## Troubleshooting

### Port Issues on Render
- Ensure your start command uses `$PORT` environment variable
- Render automatically sets the PORT variable
- The app should bind to `0.0.0.0` not `localhost`

### 404 on Root Path
- Make sure the health check endpoint is working: `GET /`
- Check the logs for startup errors

### Model Loading Issues
- Verify `HF_TOKEN` is set correctly in environment variables
- Check HuggingFace API status
- Free tier has rate limits - consider upgrading if needed

### Server Crashes
- Check Render logs for error messages
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility (3.11+ recommended)

## Development

### Project Structure
```
ai_detector_backend/
├── main.py                 # FastAPI app & configuration
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── start.sh               # Start script
├── routes/                # API route handlers
│   ├── detect_routes.py
│   ├── upload_routes.py
│   └── humanize_routes.py
├── services/              # Business logic
│   ├── ai_detector_service.py
│   ├── ai_humanize_service.py
│   └── document_service.py
└── utils/                 # Utility functions
    └── file_utils.py
```

## License

MIT