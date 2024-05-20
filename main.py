import uvicorn
from fastapi import FastAPI
from src.api_v1.document_view import router as api_router_doc
from src.api_v1.document_text_view import router as api_router_text

app = FastAPI()
app.include_router(api_router_doc)
app.include_router(api_router_text)


@app.get("/")
async def root():
    return {'status': 'True'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

