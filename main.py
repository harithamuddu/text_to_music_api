from fastapi import FastAPI, Form, Request, Header, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import soundfile as sf
import uuid
import os

#  FastAPI app
app = FastAPI(title="🎵 Secure Text-to-Music API")

#  API Key
API_KEY = "H015-0802-050-0203H"

#  Load model once
print("🎵 Loading MusicGen model…")
device = "cuda" if torch.cuda.is_available() else "cpu"

model = MusicgenForConditionalGeneration.from_pretrained(
    "facebook/musicgen-small",
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(device)

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
print(" Model Loaded Successfully!")

os.makedirs("outputs", exist_ok=True)


@app.post("/generate", response_class=HTMLResponse)
async def generate_music(
    request: Request,
    prompt: str = Form(None),
    x_api_key: str = Header(None)
):

    #  API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    #  Allow JSON + form
    if prompt is None:
        try:
            data = await request.json()
            prompt = data.get("prompt", "soft melody")
        except:
            prompt = "soft melody"

    print(f"🎶 Generating for: {prompt}")

    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)

    audio_values = model.generate(
        **inputs,
        do_sample=True,
        guidance_scale=3,
        max_new_tokens=512
    )

    sr = model.config.audio_encoder.sampling_rate

    filename = f"{uuid.uuid4().hex}.wav"
    filepath = f"outputs/{filename}"
    sf.write(filepath, audio_values[0, 0].cpu().numpy(), samplerate=sr)

    return f"""
    <html>
    <body style="background:#111; color:#fff; text-align:center; padding:50px">

        <h2>🎧 Generated Music</h2>
        <p><b>Prompt:</b> {prompt}</p>

        <audio controls autoplay style="width:80%; margin-top:20px;">
            <source src="/outputs/{filename}" type="audio/wav">
        </audio>

        <p><a href="/outputs/{filename}" download>⬇️ Download WAV</a></p>
    </body>
    </html>
    """


@app.get("/outputs/{filename}")
def get_audio(filename: str):
    return FileResponse(f"outputs/{filename}", media_type="audio/wav")
