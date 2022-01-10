from typing import List
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from main import BookmarkAnalyzer

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)

class UrlItem(BaseModel):
    url: str

class UrlQueryItem(UrlItem):
    pass

analyzer = BookmarkAnalyzer()

@app.post('/bookmark/save')
async def save_bookmark(url: UrlItem):

    result = analyzer.post_url()

    return {
        "message": "Success",
        "url": result['url'],
        "title": result['title']
    }

@app.post('/bookmark/get')
async def get_bookmark(query: UrlQueryItem):

    """Get bookmark from mongo DB
    input:
        query : Search Query : string
    
    output:
        urls : URLs list : list
    """

    pass