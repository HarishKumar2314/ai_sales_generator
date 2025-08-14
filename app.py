import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Brand Pitch Generator", page_icon="💡", layout="centered")
st.title("💡 AI Brand Pitch Generator")
st.write("Get a short, crisp pitch for any brand with best product, market trends, and key benefits.")
 
 
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"
 
 
brand_name = st.text_input("Brand Name")
product_name = st.text_input("Product Name")
tone = st.selectbox("Tone of Pitch", ["Formal", "Friendly", "Persuasive", "Excited"])
pitch_style = st.selectbox("Pitch Style", ["Short and Crisp", "Long Explanation"])
language = st.selectbox("Language", ["English", "Spanish", "French", "German"])

# Button to generate pitch
if st.button("Generate Brand Pitch"):
    if not brand_name or not product_name:
        st.warning("Please enter both Brand Name and Product Name.")
    else:
        with st.spinner("Generating your brand pitch..."):
            
            # Style instructions based on pitch style selection
            if pitch_style == "Short and Crisp":
                style_instruction = f"Write a short and crisp paragraph (max 3-4 sentences) in a {tone.lower()} tone."
            else:
                style_instruction = f"Write a longer, detailed explanation (6-8 sentences) in a {tone.lower()} tone."
            
            prompt = f"""
            You are a branding expert.
            Brand: {brand_name}
            Product: {product_name}
            Language: {language}

            {style_instruction}
            Focus on:
            - Unique strengths of the product
            - Current market relevance
            - Key benefits
            Avoid bullet points or numbering; write in natural flowing text.
            """

            try:
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(prompt)
                ai_output = response.text.strip() if hasattr(response, "text") else "No output generated."
            except Exception as e:
                ai_output = f"Error generating pitch: {e}"

            st.success("✅ Brand Pitch Generated!")
            st.markdown(ai_output)
            st.download_button(
                label="Download Pitch",
                data=ai_output,
                file_name=f"{brand_name}_{product_name}_pitch.txt",
                mime="text/plain"
            )