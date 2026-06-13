from fastapi import FastAPI
from schemas import Ingest_input

app = FastAPI(title='Content Moderator')


@app.get('/v1/ingest')
def ingest(Ingest_input):
    return 'data stored Successfully'


@app.post('/v1/text_review')
def text_review(Ingest_input):
    return 'True'


@app.post('/v1/Image_review')
def image_review(Ingest_input):
    return 'False'