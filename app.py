import streamlit as st
import uuid
import os

from storage   import load_history_from_disk, save_history_to_disk, save_image_to_disk, delete_image_from_disk
from generator import generate_content, generate_thumbnail, build_content_prompt, build_thumbnail_prompt
from styles    import get_css

# ── Session state init ────────────────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = load_history_from_disk()
if "active_id" not in st.session_state:
    st.session_state.active_id = None

# ── Page config & CSS ─────────────────────────────────────────────────────────

st.set_page_config(page_title="BlogGen", page_icon="✍️", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

# ── Left sidebar – Blog Settings ──────────────────────────────────────────────

with st.sidebar:
    st.title("🗂️ Blog Settings")
    st.subheader("Enter details of the blog you want to generate")
    blog_title = st.text_input("📝 Blog Title", placeholder="e.g. The Future of AI")
    keywords   = st.text_area("🏷️ Keywords", placeholder="e.g. AI, machine learning, technology")
    num_words  = st.slider("📊 Number of Words", min_value=250, max_value=1000, step=100)
    st.divider()
    submit_button = st.button("🚀 Generate Blog")

# ── Layout: main content (wide) + history panel (narrow) ─────────────────────

col_main, col_history = st.columns([4, 1], gap="medium")

# ── Right column – History panel ──────────────────────────────────────────────

with col_history:
    st.markdown(
        '<p style="color:#a0a0c8;font-size:0.75rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:0.08em;border-bottom:1px solid #2d2d42;padding-bottom:0.4rem;'
        'margin-bottom:0.5rem;">📋 History</p>',
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.markdown(
            '<p style="color:#55557a;font-size:0.82rem;padding:0.5rem;">No blogs generated yet.</p>',
            unsafe_allow_html=True,
        )
    else:
        for item in reversed(st.session_state.history):
            is_active = st.session_state.active_id == item["id"]
            label     = item["title"] if item["title"] else "Untitled"

            h_col1, h_col2 = st.columns([5, 1])
            with h_col1:
                btn_style = "primary" if is_active else "secondary"
                if st.button(label, key=f"load_{item['id']}", use_container_width=True, type=btn_style):
                    st.session_state.active_id = item["id"]
                    st.rerun()
            with h_col2:
                if st.button("🗑", key=f"del_{item['id']}", help="Delete this entry"):
                    delete_image_from_disk(item.get("image_path", ""))
                    st.session_state.history = [
                        h for h in st.session_state.history if h["id"] != item["id"]
                    ]
                    save_history_to_disk(st.session_state.history)
                    if st.session_state.active_id == item["id"]:
                        st.session_state.active_id = None
                    st.rerun()

# ── Main column – Header + content ────────────────────────────────────────────

with col_main:
    st.markdown("""
        <div class="main-header">
            <h1>✍️ BlogGen - Your AI blogging assistant</h1>
        </div>
    """, unsafe_allow_html=True)

    # ── Generate new blog ──────────────────────────────────────────────────────
    if submit_button:
        if not blog_title.strip():
            st.warning("Please enter a Blog Title before generating.")
        else:
            with st.spinner("🎨 Generating your thumbnail..."):
                thumbnail_bytes = generate_thumbnail(build_thumbnail_prompt(blog_title))

            with st.spinner("✍️ Writing your blog post..."):
                blog_content = generate_content(build_content_prompt(blog_title, keywords, num_words))

            entry_id   = str(uuid.uuid4())
            image_path = ""
            if thumbnail_bytes:
                image_path = save_image_to_disk(entry_id, thumbnail_bytes)

            new_entry = {
                "id":         entry_id,
                "title":      blog_title,
                "content":    blog_content,
                "image_path": image_path,
            }
            st.session_state.history.append(new_entry)
            save_history_to_disk(st.session_state.history)
            st.session_state.active_id = entry_id
            st.rerun()

    # ── Display active history item ────────────────────────────────────────────
    active = next(
        (h for h in st.session_state.history if h["id"] == st.session_state.active_id),
        None,
    )

    if active:
        img_path = active.get("image_path", "")
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        st.divider()
        st.markdown(
            f'<div class="blog-content-box">{active["content"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="footer">Generated with ✍️ BlogGen powered by Gemini</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Fill in the settings on the left and click **🚀 Generate Blog** to get started.")

