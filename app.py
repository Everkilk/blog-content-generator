import streamlit as st
import api
from google import genai
from google.genai import types

def generate_content(prompt):
    client = genai.Client(api_key=api.google_api_key)

    model = "gemini-3-flash-preview"
    response_text = ""
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text

def generate_thumbnail(prompt_thumbnail):
    client = genai.Client(api_key=api.google_api_key)

    result = client.models.generate_images(
        model="models/imagen-4.0-fast-generate-001",
        prompt=prompt_thumbnail,
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            person_generation="ALLOW_ADULT",
            aspect_ratio="16:9",
        ),
    )

    if not result.generated_images:
        print("No images generated.")
        return None

    # Save and return the image
    generated_image = result.generated_images[0]
    image_path = "generated_image.jpg"
    generated_image.image.save(image_path)
    return image_path



st.set_page_config(page_title="BlogGen", page_icon="✍️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        /* Main header */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            color: white;
        }
        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -1px;
        }
        .main-header p {
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.85;
        }

        /* Blog content box */
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

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1e1e2e;
            overflow: hidden;
        }
        section[data-testid="stSidebar"] > div:first-child {
            overflow-y: hidden;
        }
        section[data-testid="stSidebar"] * {
            color: #e0e0f0 !important;
        }
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            color: #1e1e2e !important;
        }
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
        section[data-testid="stSidebar"] .stButton button:hover {
            opacity: 0.9;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>✍️ BlogGen - Your AI blogging assistant</h1>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    # st.markdown("## 🗂️ Blog Settings")
    st.title("🗂️ Blog Settings")
    st.subheader("Enter details of the blog you want to generate")
    blog_title = st.text_input("📝 Blog Title", placeholder="e.g. The Future of AI")
    keywords = st.text_area("🏷️ Keywords", placeholder="e.g. AI, machine learning, technology")
    num_words = st.slider("📊 Number of Words", min_value=250, max_value=1000, step=100)
    st.divider()
    prompt_content = f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately{num_words}words in length, suitable for an online audience. Ensure the content is original,  informative and maintains a consistent tone throughout. \n**Effects of Generative AI: A Paradigm Shift in Technology and Creation**\n\n**Introduction**\n\nGenerative AI, an emerging field that leverages machine learning to create new and original content, is revolutionizing industries and sparking ethical debates. Its profound effects on creativity, technology innovation, and society as a whole cannot be overstated.\n\n**Artificial Creativity**\n\nGenerative AI models have demonstrated remarkable artistic abilities, generating stunning images, music, and text that rival human creations. This \"artificial creativity\" challenges our traditional notions of originality and authorship. While these models may not possess consciousness or intentionality, they can process vast amounts of data and identify patterns, resulting in surprising and often impressive outcomes.\n\n**Ethical Implications**\n\nThe advent of generative AI raises important ethical questions. Concerns about copyright infringement, job displacement, and the potential for spreading misinformation have been raised. It is crucial to develop ethical guidelines and regulations to ensure that generative AI is used responsibly, respecting human creativity and protecting the integrity of our information landscape.\n\n**Technology Innovation**\n\nGenerative AI is driving significant technological innovation. It has led to the development of novel applications in fields such as:\n\n* **Art and Design:** Creating unique digital art, fashion designs, and interior décor.\n* **Entertainment:** Generating realistic movie special effects, video game characters, and music.\n* **Healthcare:** Identifying drug targets, predicting patient outcomes, and optimizing diagnosis.\n\n**Machine Learning Applications**\n\nGenerative AI operates on powerful machine learning algorithms. By analyzing large datasets, these models learn to generate content that is both coherent and contextually relevant. Notable machine learning applications include:\n\n* **Generative Adversarial Networks (GANs):** Creating realistic images and videos from scratch.\n* **Recurrent Neural Networks (RNNs):** Generating text, code, and music sequences.\n* **Transformer Models:** Translating languages, answering questions, and summarizing text effectively.\n\n**Conclusion**\n\nThe effects of generative AI are far-reaching and transformative. It empowers us to explore uncharted realms of creativity, drives technological advancements, and challenges ethical boundaries. As this technology continues to evolve, it is imperative that we embrace its potential while carefully navigating its implications for society.\n\nGenerative AI poses both opportunities and challenges, prompting us to rethink our understanding of creativity, innovation, and the human experience. By embracing a thoughtful and balanced approach, we can harness the transformative power of this technology for the betterment of both individuals and society as a whole."
    prompt_thumbnail = f"""Generate a thumbnail image for a blog post titled \"{blog_title}\". The image should be visually appealing and relevant to the blog topic, incorporating elements that reflect the essence of the content. Ensure the design is eye-catching and suitable for online platforms, while maintaining a professional and polished look."""
    submit_button = st.button("🚀 Generate Blog")

if submit_button:
    with st.spinner("🎨 Generating your thumbnail..."):
        thumbnail = generate_thumbnail(prompt_thumbnail)
    if thumbnail:
        st.image(thumbnail, width="stretch")

    st.divider()

    with st.spinner("✍️ Writing your blog post..."):
        blog_content = generate_content(prompt_content)

    st.markdown(f'<div class="blog-content-box">{blog_content}</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer">Generated with ✍️ BlogGen powered by Gemini</div>', unsafe_allow_html=True)