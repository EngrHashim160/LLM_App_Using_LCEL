from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model=ChatGroq(model="deepseek-r1-distill-llama-70b",groq_api_key=groq_api_key)

# 1. Create Prompt Template
system_template = "Translate the following into {language}: "
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template),
     ('user', '{text}')     
])

# 2. Create a String output Parser
parser = StrOutputParser()

# 3. Create chain
chain = prompt_template|model|parser

# 4. App Definition
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using langchain runnables interfaces")

# 5. adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)