from typing import Annotated


from fastapi import Body, HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

from src.entities import AddDocuments
from src.utils.auth import verify_credentials
from src.utils.retrieval import VectorStore

TAG = "Documents"
router = APIRouter(tags=[TAG])

################################################################################
### Create New Thread
################################################################################
@router.post(
    "/documents", 
    # responses={
    #     status.HTTP_200_OK: {
    #         "description": "Add documents to the vector store.",
    #         "content": {
    #             "application/json": {
    #                 "example": AddDocuments.model_json_schema()['examples']['add_dcuments']
    #             }
    #         }
    #     }
    # }
)
def add_documents(
    body: Annotated[AddDocuments, Body()],
    username: str = Depends(verify_credentials)
):
    logger.info(f"Adding documents to the vector store: {body.documents}")
    created = VectorStore().add_docs(body.documents)
    if created:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"documents": created})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "Failed to add documents to the vector store"})
    
    
@router.delete(
    "/documents", 
    # responses={
    #     status.HTTP_200_OK: {
    #         "description": "Add documents to the vector store.",
    #         "content": {
    #             "application/json": {
    #                 "example": AddDocuments.model_json_schema()['examples']['add_dcuments']
    #             }
    #         }
    #     }
    # }
)
def delete_documents(
    body: Annotated[list[str], Body()],
    username: str = Depends(verify_credentials)
):
    logger.info(f"Deleting documents from the vector store: {body}")
    deleted = VectorStore().delete_docs(body)
    if deleted:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete documents from the vector store")