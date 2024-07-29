FROM python:3.8-slim

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir gradio ollama asyncio
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
#CMD ["docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama", "docker exec -it ollama ollama run llama2", "python", "app.py"]
CMD ["python", "app.py"]