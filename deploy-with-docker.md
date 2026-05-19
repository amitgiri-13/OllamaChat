# Deploy Using Docker Compose

This project can be run locally using Docker Compose, which starts both the chat application and Ollama model service.

---

## 1. Start the Services

Run the following command from the project root:

```bash
docker compose up
```

This will:

* Start the chat application container
* Start the Ollama service container
* Create a shared internal network between services

Note: The first run may take time as Docker pulls required images.

---

## 2. Access the Application

Once all containers are running, open your browser:

```bash
http://localhost:8000
```

This will load the chat interface.

---

## Ollama Configuration

The chat application communicates with Ollama using the internal Docker network.

### API Endpoint

```bash
http://ollama:11434
```

* `ollama` is the Docker service name
* Port `11434` is the default Ollama API port
* No external access is required for internal communication

---

## 3. Pulling Models

Before using the chat system, you must pull at least one model into Ollama.

### Example: Pull a Model

```bash
docker exec -it ollama ollama pull llama3
```

---

## Available Models

You can choose models based on your use case:

* llama3 — General purpose
* llama3.1 — Improved performance
* llama3.2 — Refined version
* mistral — Fast responses
* mixtral — Strong reasoning
* phi3 — Lightweight model
* gemma — Balanced performance
* gemma2 — Stable version
* codellama — Code generation
* deepseek-coder — Programming tasks
* deepseek-r1 — Logical reasoning
* qwen — Multilingual support
* qwen2 — Advanced reasoning
* qwen2.5-coder — Developer-focused model
* llava — Vision-capable model

---

## Environment Variables

You can configure the Ollama backend URL using environment variables.

### Default Configuration

```bash
OLLAMA_URL=http://ollama:11434
```

### Example (docker-compose.yml)

```yaml
environment:
  - OLLAMA_URL=http://ollama:11434
```

---

## Stopping the Services

To stop all running containers:

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

---

## Notes

* Ensure the Ollama container starts before sending requests.
* Models must be pulled manually unless preloaded in the image.
* If the chat UI fails to connect, verify `OLLAMA_URL` and container network.

---

