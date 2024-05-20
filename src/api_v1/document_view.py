from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_connector import get_async_session
from src.crud import crud_document
from src.schemas import DocumentModel


router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/get_all/")
async def get_all_documents_info(session: AsyncSession = Depends(get_async_session)):
    """
    Get all documents info
    :return: all objects from tabel documents
    """
    result = await crud_document.get_all_items(session)
    return result


@router.post("/upload_doc/", response_model=DocumentModel)
async def upload_doc(doc: UploadFile = File(),
                     session: AsyncSession = Depends(get_async_session)):
    """
    Upload document to project folder and create new value in database
    :return: uploaded document info
    """
    result = await crud_document.create_document(doc, session)
    return result


@router.get("/get_document/{document_id}/", response_model=DocumentModel)
async def get_documents_by_id(document_id: int,
                              session: AsyncSession = Depends(get_async_session)):
    """
    Endpoint get document by id
    :return: document info from documents table
    """
    result = await crud_document.get_item(document_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
    return result


@router.delete("/delete_doc/", response_model=DocumentModel)
async def delete_document(document_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    """
    Endpoint delete document from directory in project folder
    and remove all info and text in tables
    :param document_id:
    :param session:
    :return: deleted document info
    """
    doc_to_remove = await crud_document.get_item(document_id, session)
    await crud_document.delete_document(document_id, session)
    if doc_to_remove:
        res = await crud_document.remove_item(doc_to_remove, session)
        return res
    else:
        raise HTTPException(status_code=404, detail="Document not found")
