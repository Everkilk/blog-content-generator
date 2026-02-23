# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Keeps Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files (history/ is excluded via .dockerignore)
COPY app.py generator.py storage.py styles.py ./

# Create the history directories so the app starts cleanly
RUN mkdir -p history/images

# Streamlit listens on 8501 by default
EXPOSE 8501

# Disable Streamlit's browser-open behaviour inside a container
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]
