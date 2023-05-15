#!/usr/bin/env python3.11
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn

import urllib.parse
from dotenv import load_dotenv
import os

from functions import get_article


load_dotenv()

API_KEY = os.getenv('API_TOKEN')
API_KEY_NAME = os.getenv('API_TOKEN_NAME')

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Überprüfe deinen API Token!"
        )


api = FastAPI()


@api.get("/")
async def root(api_key: APIKey = Depends(get_api_key)):
    response = {
        "message": "Wilkommen bei der LVZ cracker API v.0.2!"
    }
    
    return response


@api.get("/get_article")
async def give_article(url: str, api_key: APIKey = Depends(get_api_key)):
    target = urllib.parse.unquote(url)
    
    a = get_article(target)
    
    response = {
        "title": a.title,
        "subtitle": a.subtitle,
        "author": a.author,
        "date": a.pub_date,
        "time": a.pub_time,
        "content": a.body_as_one(),
        "url": a.url,
        "tags": a.tags_as_string()
        }

    return response


if __name__=='__main__':
    uvicorn.run(api, host="localhost", port=8000)