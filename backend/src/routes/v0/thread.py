from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from psycopg_pool import ConnectionPool
from src.constants import DB_URI, CONNECTION_POOL_KWARGS

from src.entities import LLMHTTPResponse
from src.utils.agent import Agent
from src.utils.auth import verify_credentials

TAG = "Agent"
router = APIRouter(tags=[TAG])

################################################################################
### Query Thread History
################################################################################
@router.get(
    "/thread/{thread_id}", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All messages from existing thread.",
            "content": {
                "application/json": {
                    "example": LLMHTTPResponse.model_json_schema()['examples']['thread_history']
                }
            }
        }
    }
)
def thread_history(
    thread_id: str,
    username: str = Depends(verify_credentials)
):
    with ConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs=CONNECTION_POOL_KWARGS,
    ) as pool:
        agent = Agent(thread_id, pool)
        checkpoint = agent.checkpoint()
        response = LLMHTTPResponse(
            thread_id=thread_id, 
            messages=checkpoint.get('channel_values').get('messages')
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_200_OK
        )