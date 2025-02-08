from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from src.utils.auth import verify_credentials

TAG = "Agent"
router = APIRouter(tags=[TAG])

################################################################################
### List Tools
################################################################################
from src.tools import tools
tool_names = [{'id':tool.name, 'description':tool.description, 'args':tool.args} for tool in tools]
tools_response = {"tools": tool_names}
@router.get(
    "/tools", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All tools.",
            "content": {
                "application/json": {
                    "example": tools_response
                }
            }
        }
    }
)
def list_tools(username: str = Depends(verify_credentials)):
    return JSONResponse(
        content=tools_response,
        status_code=status.HTTP_200_OK
    )
    
################################################################################
### List Models
################################################################################
from src.constants.llm import get_available_models
@router.get(
    "/models", 
    tags=[TAG],
    responses={
        status.HTTP_200_OK: {
            "description": "All models.",
            "content": {
                "application/json": {
                    "example": {
                        "models": get_available_models()
                    }
                }
            }
        }
    }
)
def list_models(username: str = Depends(verify_credentials)):
    return JSONResponse(
        content={"models": get_available_models()},
        status_code=status.HTTP_200_OK
    )