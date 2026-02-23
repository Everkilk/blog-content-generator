def get_css() -> str:
    """Return the full page CSS as a <style> block string."""
    return """
<style>
    /* ── Main header ── */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }

    /* ── Blog content box ── */
    .blog-content-box {
        background-color: #f9f9fb;
        border-left: 5px solid #667eea;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #1e1e2e;
    }

    /* ── Left settings sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #1e1e2e;
        overflow: hidden;
    }
    section[data-testid="stSidebar"] > div:first-child { overflow-y: hidden; }
    section[data-testid="stSidebar"] * { color: #e0e0f0 !important; }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea { color: #1e1e2e !important; }
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        margin-top: 1rem;
    }
    section[data-testid="stSidebar"] .stButton button:hover { opacity: 0.9; }

    /* ── Right history column background ── */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child > div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #1e1e2e;
        border-radius: 12px;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 0.5rem 0.4rem;
    }
    /* text colors inside history column */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child p,
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child label,
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child span {
        color: #c8c8e8 !important;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
"""
