from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import datascraping
import ai_search_engine as ase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputParam(BaseModel):
    link: str
    snippet: str

class Body(BaseModel):
    search_query: str
    input_params: List[InputParam]

def fetch_summary(search_results: Body):
    scraped_result=datascraping.Data_Scraping(search_results.search_query, search_results.input_params)
    answer=ase.process_query(scraped_result['search_query'], scraped_result['parsed_documents'])
    return answer

def summarize(search_results: Body) -> str:
    return fetch_summary(search_results)

@app.post("/summarize/")
async def summarize_endpoint(search_results: Body):
    print(f"{search_results=}")
    try:
        summarized_answer = summarize(search_results)
        return summarized_answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))