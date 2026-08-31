from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AG AI backend is running 👑"
    }


@app.post("/chat")
async def chat(data: dict):

    message = data.get("message", "").strip()

    if not message:
        return {
            "error": "Message is required"
        }

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are AG AI, the intelligent assistant "
                    "for AG Empire. Be helpful, clear and friendly."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return {
        "reply": response.output_text
}
