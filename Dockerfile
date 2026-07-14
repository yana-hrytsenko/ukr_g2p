FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir ".[web]"

COPY web/ web/

ENV PORT=7860
EXPOSE 7860

CMD ["gunicorn", "app:app", "--chdir", "web", "--bind", "0.0.0.0:7860"]
