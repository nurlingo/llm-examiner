from fastapi import FastAPI
from fastapi.responses import Response
from annotations import Annotations as A
from data_extactor import extract_data_from_webpage
from llm_handler import query_llm

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Salam 3alam"}


@app.post(
    "/prodive_data_source",
    summary='Provide the url for a website to scrap and add to the knowledge base',
    description=
    'Provide the URL for web content, which will be used as knowledge database for future question creation. '
    'Content will be scrapped from URL and all subpages recursively and converted to knowledge database.'
    '\n\n'
    'Provided knowledge_base_id will be associated with created knowledge database.'
    '\n\n'
    'To check for existing knowledge databases and their respective IDs, '
    'see `/api/v1/content/list` (not implemented).'
)
async def extract_data_from_web_data_source(
    knowledge_base_id: A.knowledge_base_id,
    url: A.url
):
    if extract_data_from_webpage(knowledge_base_id=knowledge_base_id, url=url):
        return Response(status_code=200)
    else:
        return Response(status_code=400)
    

@app.post(
    "/generate_activity",
    summary='Generate an assessment activity for a given outcome and a knowledge database',
    description=
    'Generate an assessment activity of questions for the given knowledge base.'
    'If no knowledge is associated with given ID, returns an error.'
)
async def generate_activity(
    knowledge_base_id: A.knowledge_base_id,
    outcome: A.outcome,
    number_of_questions: A.number_of_questions,
    question_types: A.question_types
) -> str:
    return query_llm(knowledge_base_id, outcome, number_of_questions, question_types)
