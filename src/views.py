from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_connector import get_async_session
from src.crud import crud_document, crud_document_text
from src.schemas import DocumentModel, DocumentText
from src.tasks import task_analyze_document

# router = APIRouter(prefix="/documents", tags=["documents"])
#
#
# @router.get("/get_all/")
# async def get_all_documents_info(session: AsyncSession = Depends(get_async_session)):
#     result = await crud_document.get_all_items(session)
#     return result
#
#
# @router.post("/upload_doc/", response_model=DocumentModel)
# async def upload_doc(doc: UploadFile = File(),
#                      session: AsyncSession = Depends(get_async_session)):
#     result = await crud_document.create_document(doc, session)
#     return result
#
#
# @router.get("/get_document/{document_id}/", response_model=DocumentModel)
# async def get_documents_by_id(document_id: int,
#                               session: AsyncSession = Depends(get_async_session)):
#     result = await crud_document.get_item(document_id, session)
#     if not result:
#         raise HTTPException(status_code=404, detail="Document not found")
#     return result
#
#
# @router.delete("/delete_doc/", response_model=DocumentModel)
# async def delete_document(document_id: int,
#                           session: AsyncSession = Depends(get_async_session)):
#     doc_to_remove = await crud_document.get_item(document_id, session)
#     await crud_document.delete_document(document_id, session)
#     if doc_to_remove:
#         res = await crud_document.remove_item(doc_to_remove, session)
#         return res
#     else:
#         raise HTTPException(status_code=404, detail="Document not found")
#
#
# @router.post("/document_analyze/{document_id}")
# async def document_img_to_text(document_id: int,
#                                session: AsyncSession = Depends(get_async_session)):
#     document_info = await crud_document.get_item(document_id, session)
#     if document_info:
#         text = task_analyze_document.delay(str(document_info.path))
#         text = str(text.get(timeout=1000))
#         result = await crud_document_text.document_analyze(document_id,
#                                                            text.replace('\n', ''),
#                                                            session)
#         return result
#     else:
#         raise HTTPException(status_code=404, detail="Document not found")
#
#
# @router.get("/get_doc_text/{document_id}/", response_model=DocumentText)
# async def get_document_analyze_text(document_id: int,
#                                     session: AsyncSession = Depends(get_async_session)):
#     document_info = await crud_document_text.get_doc_text(document_id, session)
#     if document_info:
#         return document_info
#     else:
#         raise HTTPException(status_code=404, detail="Document not found")
