import streamlit as st
from PIL import Image
import google.generativeai as genai

from datetime import date

# Ensure the API key is configured
genai.configure(api_key="AIzaSyCcNOie26_Mm7npTI-rGBBbywfTeAal5eQ")
model = genai.GenerativeModel('gemini-1.5-flash')

class TrashClassificationModel:
    def __init__(self):
        self.input_prompt = """
            You are an expert in identifying types of trash. 
            You will receive an image as input, and your task is to classify it into one of the following categories: 
            plastic, glass, metal, paper, organic, medical, nuclear waste. If it's not trash, return "Not Trash".
            """

    # Function to get the response for image input
    def get_gemini_response_image(self, image, prompt):
        response = model.generate_content([image[0], prompt])
        return response.text

    # Function to set up image data for processing
    def input_image_setup(self, uploaded_file):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")

    def classify_trash(self, uploaded_file):
        image_data = self.input_image_setup(uploaded_file)
        response = self.get_gemini_response_image(image_data, self.input_prompt)
        return response

def main():
    st.set_page_config(page_title="Trash Classification Demo")
    st.title("Trash Classification Tool")

    uploaded_file = st.file_uploader("Upload an image of trash...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

        trash_model = TrashClassificationModel()
        classification_result = trash_model.classify_trash(uploaded_file)

        st.subheader("Classification Result")
        st.write(classification_result)

if __name__ == "__main__":
    main()
