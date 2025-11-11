# Render Deployment Guide

## Pre-Deployment Checklist

- [ ] HuggingFace account created
- [ ] HuggingFace API token generated (https://huggingface.co/settings/tokens)
- [ ] Code pushed to GitHub repository
- [ ] Render account created (https://render.com)

## Deployment Steps

### 1. Create New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `ai_detector_backend` repository

### 2. Configure Service

**Basic Settings:**
- **Name**: `ai-detector-backend` (or your preferred name)
- **Region**: Choose closest to your users (e.g., Oregon)
- **Branch**: `main` (or your default branch)
- **Runtime**: Python 3

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **Free** tier

### 3. Environment Variables

Add the following environment variable:

| Key | Value | Notes |
|-----|-------|-------|
| `HF_TOKEN` | `your_token_here` | Get from https://huggingface.co/settings/tokens |

**Important**: Keep this token secret! Don't commit it to your repository.

### 4. Deploy

1. Click "Create Web Service"
2. Wait for the build to complete (2-5 minutes)
3. Check the logs for any errors

## Expected Deployment Logs

You should see logs similar to:
```
==> Building...
Successfully installed fastapi uvicorn huggingface_hub nltk...
==> Deploying...
==> Running 'uvicorn main:app --host 0.0.0.0 --port 10000'
INFO:     Started server process [56]
INFO:     Waiting for application startup.
🔄 Initializing AI detector client...
✅ AI detector client initialized!
🔄 Initializing text humanizer client...
ℹ️  Text humanizer is using placeholder implementation
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

## Testing Your Deployment

### 1. Health Check

Once deployed, your app will be available at: `https://your-app-name.onrender.com`

Test the health endpoint:
```bash
curl https://your-app-name.onrender.com/
```

Expected response:
```json
{
  "status": "healthy",
  "message": "AI Text Detector API is running",
  "version": "2.0",
  "endpoints": {
    "health": "/",
    "docs": "/docs",
    "detect_text": "/api/detect",
    "upload_file": "/api/upload",
    "humanize_text": "/api/humanize"
  },
  "models": {
    "detector": "openai-community/roberta-base-openai-detector",
    "humanizer": "google/flan-t5-base (placeholder)"
  }
}
```

### 2. Test Detection Endpoint

```bash
curl -X POST https://your-app-name.onrender.com/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test sentence to check if the AI detector works."}'
```

### 3. Use the Test Script

```bash
# Install requests if not already installed
pip install requests

# Test local server
python test_endpoints.py http://localhost:8000

# Test deployed server
python test_endpoints.py https://your-app-name.onrender.com
```

### 4. Interactive API Documentation

Visit: `https://your-app-name.onrender.com/docs`

This provides a Swagger UI where you can test all endpoints interactively.

## Common Issues & Solutions

### Issue: Port scan timeout

**Symptoms:**
```
Port scan timeout reached, failed to detect open port 8000
```

**Solution:**
- Ensure start command uses `$PORT`: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- The `render.yaml` file handles this automatically
- Don't hardcode port numbers in the start command

### Issue: 404 on root path

**Symptoms:**
```
INFO: 127.0.0.1:56370 - "HEAD / HTTP/1.1" 404 Not Found
```

**Solution:**
- This is now fixed with the health check endpoint at `/`
- Render uses HEAD requests to check if the service is up

### Issue: Server crashes on startup

**Symptoms:**
- Service shows "Deploy failed"
- Logs show Python errors

**Solutions:**
1. Check `HF_TOKEN` is set correctly
2. Verify all dependencies are in `requirements.txt`
3. Check Python version compatibility
4. Review logs for specific error messages

### Issue: Free tier spin-down

**Symptoms:**
- First request after inactivity is slow (30-60 seconds)

**Solution:**
- This is expected behavior on free tier
- Service spins down after 15 minutes of inactivity
- Consider upgrading to paid tier for always-on service
- Or use a cron job to ping the health endpoint every 10 minutes

### Issue: Rate limiting from HuggingFace

**Symptoms:**
- 429 Too Many Requests errors
- Slow response times

**Solutions:**
1. HuggingFace free tier has rate limits
2. Consider upgrading to HuggingFace Pro
3. Implement request caching
4. Add rate limiting to your API

## Monitoring

### View Logs

1. Go to your service dashboard on Render
2. Click "Logs" tab
3. Monitor for errors or warnings

### Health Checks

Render automatically monitors your service using the root endpoint (`/`).

If the health check fails, Render will:
- Mark the service as unhealthy
- Attempt to restart the service
- Send notifications (if configured)

## Updating Your Deployment

### Automatic Deploys

By default, Render automatically deploys when you push to your main branch:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically:
1. Detect the push
2. Build the new version
3. Deploy if build succeeds
4. Keep the old version running until new version is ready

### Manual Deploys

1. Go to your service dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

## Rollback

If a deployment fails:

1. Go to "Events" tab
2. Find the last successful deployment
3. Click "Rollback to this version"

## Environment Variables Management

To update environment variables:

1. Go to "Environment" tab
2. Update the variable value
3. Click "Save Changes"
4. Service will automatically redeploy

## Cost Optimization (Free Tier)

- ✅ Use HuggingFace Inference API (no model storage needed)
- ✅ Lightweight dependencies
- ✅ No database required
- ✅ Minimal memory footprint
- ⚠️ Service spins down after 15 min inactivity
- ⚠️ 750 hours/month free (enough for one always-on service)

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test all endpoints
3. 📱 Connect your frontend
4. 🔒 Add authentication (if needed)
5. 📊 Set up monitoring/analytics
6. 🚀 Consider upgrading for production use

## Support

- Render Docs: https://render.com/docs
- HuggingFace Docs: https://huggingface.co/docs
- FastAPI Docs: https://fastapi.tiangolo.com

## Security Notes

- ⚠️ Never commit `HF_TOKEN` to git
- ⚠️ Use environment variables for all secrets
- ⚠️ Consider adding rate limiting for production
- ⚠️ Add authentication for sensitive endpoints
- ⚠️ Enable CORS only for trusted domains in production

