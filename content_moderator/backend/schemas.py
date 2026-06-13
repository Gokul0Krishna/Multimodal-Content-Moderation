from pydantic import BaseModel,HttpUrl

class Ingest_input(BaseModel):
    text: str
    img : HttpUrl
    
    