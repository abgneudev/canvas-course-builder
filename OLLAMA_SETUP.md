# Ollama Setup Guide

## ✅ Migration Complete!

Your Canvas AI Assistant now uses **Ollama** (local LLM) instead of Groq/Gemini.

## Prerequisites

### 1. Install Ollama
Download from: https://ollama.com/download

**Windows:**
- Download and run the installer
- Ollama will start automatically

**Verify installation:**
```powershell
ollama --version
```

### 2. Pull the Model
```powershell
ollama pull llama3.2
```

This downloads the Llama 3.2 model (~2GB). Other options:
- `llama3.2:1b` - Smallest, fastest
- `llama3.2` - Default (3B parameters)
- `llama3.1:8b` - Larger, more capable

### 3. Start Ollama Server
Ollama should start automatically. If not:
```powershell
ollama serve
```

The server runs on `http://localhost:11434`

## Running Your App

### 1. Ensure Ollama is Running
Check if Ollama is running:
```powershell
curl http://localhost:11434
```

Should return: `Ollama is running`

### 2. Start the Streamlit App
```powershell
streamlit run app.py
```

## What Changed

### Code Changes
- **gemini_service.py**: Now uses OpenAI client with Ollama endpoint
- **app.py**: Removed API key requirement (Ollama runs locally)
- **requirements.txt**: Changed from `groq` to `openai` package

### Configuration Changes
- **No API key needed** - Ollama runs entirely on your machine
- **Model**: Changed to `llama3.2` (local)
- **Endpoint**: `http://localhost:11434/v1`

### Benefits
✅ **Privacy**: All processing happens locally  
✅ **No costs**: No API usage fees  
✅ **Offline**: Works without internet (after model download)  
✅ **Fast**: Local inference with good hardware  

## Switching Models

To use a different model, edit [gemini_service.py](gemini_service.py):

```python
self.model_name = 'llama3.2'  # Change this
```

Available models:
```powershell
ollama list
```

Pull more models:
```powershell
ollama pull mistral
ollama pull codellama
ollama pull llama3.1:8b
```

## Troubleshooting

### "Connection refused" error
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is available

### Model not found
- Pull the model first: `ollama pull llama3.2`
- Check available models: `ollama list`

### Slow responses
- Llama 3.2 requires decent hardware (8GB+ RAM recommended)
- Try smaller model: `ollama pull llama3.2:1b`
- Close other applications to free up resources

### Function calling issues
- Ollama supports OpenAI-compatible tool calling
- If tools aren't working, update Ollama: `ollama pull llama3.2`

## Performance Tips

1. **GPU Acceleration**: Ollama automatically uses GPU if available (NVIDIA/AMD)
2. **RAM**: Keep at least 4GB free for the model
3. **Model Selection**: 
   - `llama3.2:1b` - Fast, basic tasks
   - `llama3.2` - Balanced (recommended)
   - `llama3.1:8b` - Better quality, slower

## Environment Variables

Your `.env` file should now look like:
```env
# Ollama Configuration (runs locally - no API key needed)

# Canvas LMS Configuration
CANVAS_API_TOKEN=your_canvas_token
CANVAS_BASE_URL=https://canvas.instructure.com
```

## Next Steps

1. **Test basic queries**: "List my courses"
2. **Try function calling**: "Create a page called 'Welcome' in course 12345"
3. **Build modules**: "Create a module called 'Week 1' with 3 pages"

## Reverting to Groq/Gemini

If you need to switch back:
1. Restore `gemini_service_old.py` 
2. Update `requirements.txt` to use `groq` or `google-genai`
3. Add API key back to `.env`

## Resources

- **Ollama Docs**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.com/library
- **OpenAI Compatibility**: https://github.com/ollama/ollama/blob/main/docs/openai.md
