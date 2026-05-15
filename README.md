# Ollama Chat App

This is a simple web-based chat application built using FastAPI and Ollama. It allows users to interact with locally running AI models through a web interface.

## Demo 

![alt text](./images/demo1.png)

## Project Structure

```
.
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
└── src
    ├── main.py
    ├── requirements.txt
    ├── static
    └── templates
        └── index.html

```

## Features

- Web-based chat interface
- Integration with local Ollama models
- FastAPI backend and Simple frontend using HTML templates
- Docker support for easy deployment

## Requirements

- Docker
- Docker Compose
- Ollama installed or running in a container

## Setup and Run

### Using Docker Compose

1. Start the services:

```bash
docker compose up 
```
It might take some time to pull the images, depending upon your internet connection.


2. Open the application in your browser:

```bash
http://localhost:8000
```

## Ollama Configuration

The application connects to Ollama using the API endpoint:

```bash 
http://ollama:11434
```

Make sure the Ollama container is running before using the chat interface. Now you need to pull a model to use.

To pull a model:

```bash
docker exec -it ollama ollama pull llama3
```

Models you can pull: 
* llama3: General
* llama3.1: Improved
* llama3.2: Refined
* mistral: Fast
* mixtral: Reasoning
* phi3: Lightweight
* gemma: Balanced
* gemma2: Stable
* codellama: Coding
* deepseek-coder: Programming
* deepseek-r1: Logic
* qwen: Multilingual
* qwen2: Advanced
* qwen2.5-coder: Developer
* llava: Vision

## Environment Variables

You can configure the Ollama URL using:

```bash
OLLAMA_URL=http://ollama:11434
```

## License

This project is licensed under the MIT License.

---
