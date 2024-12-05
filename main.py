from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

broken_text = [
    "Lorem ipsum dolor sit amet",
    "consectetur adipiscing elit",
    "sed do eiusmod tempor incididunt",
    "ut labore et dolore magna aliqua",
    ]

async def get_text_stream(size, id):
    
    # generate static text for the event stream
    # and push that to the client
    for i in range(size):
        data = json.dumps(broken_text[i % len(broken_text)])
        yield f"id: {i}\nevent: message\ndata: {data}\n\n"
        # sleep to simulate a slow stream
        await sleep(1)
        
    # not a necessary event, but an information to the client that the streaming is complete, 
    # and the client likely closes the event stream
    yield f"event: terminate\ndata: text streaming complete\n\n"

@app.get("/sr")
async def root(size: int = 10, id: int = 1):
    return StreamingResponse(get_text_stream(size, id), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)