from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from transcriber import transcribe_audio
from summarizer import summarize_text
import os

app = FastAPI()

@app.post("/summarize")
async def summarize_meeting(audio: UploadFile = File(...)):
    temp_file_path = f"temp_{audio.filename}"

    with open(temp_file_path, "wb") as f:
        f.write(await audio.read())

    try:
        transcript = transcribe_audio(temp_file_path)
        summary = summarize_text(transcript)

        return JSONResponse(content={
            "transcript": transcript,
            "summary": summary
        })
    finally:
        os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
