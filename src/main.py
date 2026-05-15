import os
import json
import httpx
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI(title="Ollama Chat")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# Ollama Configuration
# =========================
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"
DEFAULT_MODEL = "llama3"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/models")
async def get_models():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(OLLAMA_TAGS_URL)
            response.raise_for_status()
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            return {"models": models or [DEFAULT_MODEL]}
    except Exception as e:
        return {"models": [DEFAULT_MODEL], "error": str(e)}


@app.post("/chat/stream")
async def chat_stream(
    prompt: str = Form(...),
    model: str = Form(DEFAULT_MODEL),
    history: Optional[str] = Form(None),  # JSON array of {role, content}
):
    """
    Stream a response from Ollama using the /api/chat endpoint,
    which supports multi-turn conversation history.

    `history` should be a JSON string like:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """

    # Parse conversation history sent from the frontend
    messages = []
    if history:
        try:
            past = json.loads(history)
            for msg in past:
                role = msg.get("role", "user")
                # Ollama uses "assistant" not "ai"
                if role == "ai":
                    role = "assistant"
                messages.append({"role": role, "content": msg.get("content", "")})
        except (json.JSONDecodeError, TypeError):
            pass

    # Append the current user prompt
    messages.append({"role": "user", "content": prompt})

    async def generate():
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST", OLLAMA_CHAT_URL, json=payload
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            chunk = json.loads(line)
                            # /api/chat returns tokens inside message.content
                            token = chunk.get("message", {}).get("content", "")
                            done = chunk.get("done", False)

                            yield (
                                f"data: {json.dumps({'token': token, 'done': done})}\n\n"
                            )
                            if done:
                                break
                        except json.JSONDecodeError:
                            continue

        except httpx.ConnectError:
            yield (
                f"data: {json.dumps({'token': '[Error: Cannot connect to Ollama. Make sure it is running.]', 'done': True})}\n\n"
            )
        except httpx.HTTPStatusError as e:
            # Fall back to /api/generate if /api/chat isn't supported
            if e.response.status_code == 404:
                async for chunk in _fallback_generate(model, prompt):
                    yield chunk
            else:
                yield (
                    f"data: {json.dumps({'token': f'[HTTP Error: {e.response.status_code}]', 'done': True})}\n\n"
                )
        except Exception as e:
            yield (
                f"data: {json.dumps({'token': f'[Error: {str(e)}]', 'done': True})}\n\n"
            )

    return StreamingResponse(generate(), media_type="text/event-stream")


async def _fallback_generate(model: str, prompt: str):
    """Fallback to /api/generate for older Ollama versions."""
    payload = {"model": model, "prompt": prompt, "stream": True}
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST", OLLAMA_GENERATE_URL, json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        done = chunk.get("done", False)
                        yield f"data: {json.dumps({'token': token, 'done': done})}\n\n"
                        if done:
                            break
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield f"data: {json.dumps({'token': f'[Fallback error: {str(e)}]', 'done': True})}\n\n"