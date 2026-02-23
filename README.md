# ✍️ BlogGen — AI Blog Content Generator

BlogGen is a web app that generates complete blog posts with AI-written content and a matching thumbnail image, powered by Google Gemini.

---

## 🛠️ Libraries Used

- **[Streamlit](https://streamlit.io/)** — builds the interactive web UI with no frontend code required
- **[Google GenAI (`google-genai`)](https://ai.google.dev/)** — two models are used:
  - `gemini-3-flash-preview` — generates the blog post content with Google Search grounding for up-to-date information
  - `imagen-4.0-fast-generate-001` — generates a 16:9 thumbnail image matching the blog topic

---

## 🔄 Project Flow

1. User fills in **Blog Title**, **Keywords**, and **Word Count** in the left sidebar
2. Clicking **🚀 Generate Blog** sends two parallel requests to Google's API:
   - The thumbnail image is generated first
   - The blog content is streamed and assembled
3. The result (image + content) is displayed in the main area
4. The entry is automatically **saved to disk** (`history/history.json` + `history/images/`)

---

## 📋 History

Every generated blog is saved locally and persists across restarts. The **right-side history panel** lists all previous blogs by title. Click any entry to reload it, or click 🗑 to permanently delete it (removes both the metadata and the image file).

---

## 🐳 Docker Setup

**Pull and run from Docker Hub:**
```bash
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY="your_google_api_key" \
  -v $(pwd)/history:/app/history \
  everkilk/bloggen:latest
```

**Or build locally with docker-compose:**
```bash
# 1. Set your API key
export GOOGLE_API_KEY="your_google_api_key"   # Windows: $env:GOOGLE_API_KEY="..."

# 2. Build and start
docker compose up --build
```

Open `http://localhost:8501` in your browser.

> The `history/` folder is mounted as a volume so your generated blogs and images are saved on your machine, not inside the container.

---

## ⚙️ Local Setup (without Docker)

```bash
git clone https://github.com/everkilk/blog-content-generator
cd blog-content-generator
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
# Add your API key to api.py or set GOOGLE_API_KEY env var
.venv\Scripts\streamlit run app.py
```
