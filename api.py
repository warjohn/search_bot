import os
from autorag.deploy import Runner
from pydantic import BaseModel
import autorag
from llama_index.embeddings.ollama import OllamaEmbedding
from autorag import LazyInit
from fastapi import FastAPI, HTTPException
import uvicorn
import nest_asyncio

nest_asyncio.apply()
app = FastAPI()

ollama = autorag.embedding_models['ollama'] = LazyInit(OllamaEmbedding, model_name="llama3.1")
runner = Runner.from_yaml(r'data_original/test_1/pipline.yaml', project_dir=r"data_original/test_1")

class QueryRequest(BaseModel):
    query: str

@app.post("/run_query/")
async def run_query(request: QueryRequest):

    result = runner.run(query=request.query)
    return {
        "result": result
    }

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8030, loop="asyncio")



