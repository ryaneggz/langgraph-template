## https://www.softgrade.org/sse-with-fastapi-react-langgraph/
import os

from fastapi import FastAPI
from dotenv import load_dotenv

from src.routes import router
load_dotenv()

# Define the FastAPI app
app = FastAPI(
    title="LangGraph API Starter 🤖",
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
    docs_url="/"
)

# Include the router
app.include_router(router)

### Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=str(os.getenv("HOST", "0.0.0.0")), 
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )