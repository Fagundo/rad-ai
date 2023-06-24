import logging
from typing import Union
from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

# Create app and load summarizer
app = FastAPI()
app.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class SummaryRequest(BaseModel):
    text: str
    summary_length: int

@app.post("/summary")
def read_item(summary: SummaryRequest):
    summary = app.summarizer(summary.text, max_length=summary.summary_length, min_length=10)
    summary = summary[0]['summary_text']

    return {"summary": summary}
