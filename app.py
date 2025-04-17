import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from agno.agent import Agent
from agno.models.groq import Groq
import re

# 🌟 Set Up the AI Agent with Groq
model = Groq("llama3-70b-8192", api_key="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")
agent = Agent(model=model)

# 🛒 Shopping Assistant Function

def shopping_assistant(query):
    prompt = f"""
    You are a helpful and friendly shopping assistant.
    Help the user find the best product matching this query: "{query}"
    Return a markdown-formatted recommendation.
    Avoid using phrases like 'Top Pick:' or 'Buy Now:'.
    """
    response = agent.run(prompt)
    cleaned_response = re.sub(r'(Top Pick:|Buy Now:.*?)\n?', '', response.content, flags=re.IGNORECASE)
    return cleaned_response.strip() if response else "Sorry, I couldn't find any results. Please try again."

# 🎨 Logo to Base64 for Sidebar
def get_base64_logo(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def main():
    st.set_page_config(page_title="Smart Shopping Assistant", layout="wide")

    # Inject Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        [data-testid="stSidebar"] {
            width: 320px !important;
            background: linear-gradient(to bottom right, #003D62, #3497BA);
            color: white;
            padding: 20px;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p {
            color: white !important;
        }

        h1, h2, h3, h4, h5, h6, p {
            font-family: 'Poppins', sans-serif;
        }

        img {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Logo and Sidebar Content
    try:
        logo_base64 = get_base64_logo("Static/Hoonartek-V25-White-Color.png")
        st.sidebar.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 220px; margin-bottom: 20px; border-radius: 0px;" />
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.sidebar.warning("Logo not found or failed to load.")

    st.sidebar.title("Use Case Details")
    st.sidebar.markdown("This shopping assistant provides friendly answers and personalized support. This Model is perfect for enhancing websites or customer service systems.")
    st.sidebar.header("Model Name:")
    st.sidebar.markdown("Groq LLaMA3 70B")

    # Main UI
    st.markdown("""
    <h1 style='font-size: 30px; color: #2f729b; margin-bottom: 20px; text-align: center'>
        Smart Shopping Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='font-size: 20px; color: #2f729b; margin-bottom: 20px; text-align: center'>
    Welcome to the Smart Shopping Assistant!  
    I will help you to buy the best product!
    </h2>
    """, unsafe_allow_html=True)

    query = st.text_input("Enter a product details:", placeholder="e.g., Asus ZenBook 14", key="product_query")

    if query:
        with st.spinner("Searching for products..."):
            results = shopping_assistant(query)
            st.markdown("### Product Results")
            st.markdown(results)

# 🚀 Run App
if __name__ == "__main__":
    main()
