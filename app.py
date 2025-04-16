import requests
import streamlit as st
from PIL import Image
from io import BytesIO
import base64

# API Keys
GEMINI_API_KEY = "AIzaSyAVwoZmGiYvSj8sbD2wOAvjI3f1crjT9hU"
SERPAPI_API_KEY = "4237ce6a76722c312bd2f1f8b26b71f9ca86bc080a82d3e282b0df4eda4caa62"

# Currency conversion (USD to INR)
USD_TO_INR = 83.5


# 🛍️ Fetch Shopping Results
def get_shopping_results(query):
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code == 200:
        results = response.json()
        return results.get("shopping_results", [])
    else:
        st.error("Failed to fetch results from SerpAPI. Please try again later.")
        return []


# 🎨 Logo to Base64 for Sidebar
def get_base64_logo(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# 💡 Shopping Assistant Logic
def shopping_assistant(query):
    shopping_results = get_shopping_results(query)

    if not shopping_results:
        return f"No shopping results found for '{query}'. Please try a more specific product."

    result_summary = f"Found {len(shopping_results)} shopping results for '{query}'.\n\n"
    result_summary += "### 🔝 Top 3 Results:\n\n"

    for i, item in enumerate(shopping_results[:3]):
        title = item.get("title", "N/A")
        link = item.get("link", "#")
        source = item.get("source", "N/A")
        price = item.get("price", "$0").replace("$", "")
        image_url = item.get("thumbnail", "")

        try:
            price_inr = round(float(price.replace(",", "")) * USD_TO_INR, 2)
            price_display = f"₹{price_inr:,.2f}"
        except:
            price_display = "Price not available"

        result_summary += f"**{i+1}. {title}**\n"
        result_summary += f"- 💰 **Price**: {price_display}\n"
        result_summary += f"- 🌐 **Source**: {source}\n"
        result_summary += f"- 🔗 [View Product]({link})\n"
        result_summary += f"- 🖼️ ![Product Image]({image_url})\n\n"

    return result_summary


# 🌐 Streamlit App UI
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

    st.sidebar.title("Smart Shopping Agent")
    st.sidebar.markdown("This shopping assistant provides friendly answers and personalized support. This Model is perfect for enhancing websites or customer service systems.")
    st.sidebar.header("Model Used:")
    st.sidebar.markdown("Google SerpApi and Gemini 2.0 Flash")

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

    query = st.text_input("Enter a product name:", placeholder="e.g., Dell XPS 13 Laptop", key="product_query")

    if query:
        with st.spinner("Searching for products..."):
            results = shopping_assistant(query)
            st.markdown(results)


# 🚀 Run App
if __name__ == "__main__":
    main()
