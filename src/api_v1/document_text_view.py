from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_connector import get_async_session
from src.crud import crud_document, crud_document_text
from src.schemas import DocumentText
from src.tasks import task_analyze_document

router = APIRouter(prefix='/text_analyze', tags=['text_analyze'])


@router.post("/document_analyze/{document_id}/")
async def document_img_to_text(document_id: int,
                               session: AsyncSession = Depends(get_async_session)):
    """
    Endpoint find document by id and performs celery task of translating text on image
    to string and save received result in table document_text
    :param document_id: id of document to be translated
    :param session: async session
    :return: object info from document_text table
    """
    document_info = await crud_document.get_item(document_id, session)
    if not document_info:
        raise HTTPException(status_code=404, detail="Document not found")

    exist = await crud_document_text.get_doc_text(document_id, session)
    if exist:
        raise HTTPException(status_code=409, detail="Document already exists")

    text = task_analyze_document.delay(str(document_info.path))
    text = str(text.get(timeout=1000))
    result = await crud_document_text.document_analyze(document_id,
                                                       text.replace('\n', ' '),
                                                       session)
    return result


@router.get("/get_doc_text/{document_id}/", response_model=DocumentText)
async def get_document_analyze_text(document_id: int,
                                    session: AsyncSession = Depends(get_async_session)):
    """
    Endpoint received document id and show text on document
    :return: text on document
    """
    document_info = await crud_document_text.get_doc_text(document_id, session)
    if document_info:
        return document_info
    else:
        raise HTTPException(status_code=404, detail="Document not found")
