# app.py

from api import app  # Import FastAPI app from api.py

# Optional: Uvicorn entry point for running app.py directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
