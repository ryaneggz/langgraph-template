## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles 
from dotenv import load_dotenv

from src.constants import APP_PORTAL_ENABLED
from src.routes.v0 import tool, llm, thread, retrieve, source
load_dotenv()

# Define the FastAPI app
app = FastAPI(
    title="Thread Agent by Prompt Engineers AI 🤖",
    version=os.getenv("APP_VERSION", "0.1.0"),
    description=(
        "This is a simple API for building chatbots with LangGraph. " +
        "It allows you to create new threads, query existing threads, " +
        "and get the history of a thread.\n Check out the repo on " +
        f"<a href='https://github.com/ryaneggz/langgraph-template'>Github</a>"
    ),
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True,
    docs_url="/api"
)

# Include the router
app.include_router(llm)
app.include_router(thread)
app.include_router(tool)
app.include_router(retrieve)
app.include_router(source)

# Mount the MkDocs static site
public_dir = Path("src/public")
docs_dir = Path("src/site")

# Mount the public directory if it exists (for React app)
if APP_PORTAL_ENABLED and public_dir.exists():
    app.mount("/", StaticFiles(directory="src/public", html=True), name="public")
else:
    # Mount docs as root if no portal
    app.mount("/", StaticFiles(directory="src/site", html=True), name="site")

# API Landing Page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home():
    if APP_PORTAL_ENABLED and public_dir.exists():
        return FileResponse(public_dir / "index.html")
    else:
        return FileResponse(docs_dir / "index.html")

# API Landing Page
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def documentation():
    return FileResponse(docs_dir)

### Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=str(os.getenv("HOST", "0.0.0.0")), 
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )
