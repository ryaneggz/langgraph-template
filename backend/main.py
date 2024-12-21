import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware

from src.routes.v0 import tool, llm, thread, retrieve, source
from src.constants import (
    HOST,
    PORT,
    LOG_LEVEL,
    APP_VERSION,
    APP_PORTAL_ENABLED
)

app = FastAPI(
    title="Thread Agent by Prompt Engineers AI 🤖",
    version=APP_VERSION,
    description=(
        "This is a simple API for building chatbots with LangGraph. " 
        "It allows you to create new threads, query existing threads, "
        "and get the history of a thread.\n Check out the repo on "
        f"<a href='https://github.com/ryaneggz/langgraph-template'>Github</a>"
    ),
    contact={
        "name": "Ryan Eggleston",
        "email": "ryaneggleston@promptengineers.ai"
    },
    debug=True,
    docs_url="/api"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(llm)
app.include_router(thread)
app.include_router(tool)
app.include_router(retrieve)
app.include_router(source)

public_dir = Path("src/public")
docs_dir = Path("src/public/docs")

# If portal is enabled and public directory exists, serve the React app at "/"
if APP_PORTAL_ENABLED and public_dir.exists():
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
else:
    # If no portal, serve mkdocs at root
    app.mount("/", StaticFiles(directory=docs_dir, html=True), name="site")

# Home endpoint
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home():
    if APP_PORTAL_ENABLED and public_dir.exists():
        return FileResponse(public_dir / "index.html")
    else:
        return FileResponse(docs_dir / "index.html")

### Run Server
if __name__ == "__main__":
    import uvicorn
    
    print(f"Environment Settings:")
    print(f"LOG_LEVEL: {LOG_LEVEL}")
    print(f"APP_PORTAL_ENABLED: {APP_PORTAL_ENABLED}")
    
    
    print(f"Configuration Settings:")
    print(f"Public Dir Exists: {public_dir.exists()}")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT, 
        log_level=LOG_LEVEL
    )
