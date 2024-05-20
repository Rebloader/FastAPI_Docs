import os
import shutil
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import BASE_DIR
from src.model import Document, DocumentText


class CRUD:
    def __init__(self, model):
        self.model = model

    async def get_all_items(self, session: AsyncSession):
        items = await session.execute(select(self.model).order_by(self.model.id))
        return items.scalars().all()

    async def get_item(self, id_doc: int, session: AsyncSession):
        db_item = await session.get(self.model, id_doc)
        return db_item

    async def remove_item(self, db_item, session: AsyncSession):
        await session.delete(db_item)
        await session.commit()
        return db_item


class DocumentCRUD(CRUD):
    async def create_document(self, document_in, session: AsyncSession):
        save_path = f'{BASE_DIR}/documents/{document_in.filename}'
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(document_in.file, f)

        db_item = self.model(path=document_in.filename, date=datetime.now())
        session.add(db_item)
        await session.commit()

        return db_item

    async def delete_document(self, id_doc: int, session: AsyncSession):
        file = await session.execute(select(self.model.path).where(self.model.id == id_doc))
        file = file.scalars().first()
        full_path = f'{BASE_DIR}/documents/{file}'
        if os.path.exists(full_path):
            os.remove(full_path)


class DocumentTextCRUD(CRUD):
    async def document_analyze(self, id_doc: int, text: str, session: AsyncSession):
        document_in = self.model(id_doc=id_doc, text=text)
        session.add(document_in)
        await session.commit()
        return document_in

    async def get_doc_text(self, id_doc: int, session: AsyncSession):
        db_item = await session.execute(select(self.model).where(self.model.id_doc == id_doc))
        return db_item.scalar_one_or_none()


crud_document = DocumentCRUD(Document)
crud_document_text = DocumentTextCRUD(DocumentText)
