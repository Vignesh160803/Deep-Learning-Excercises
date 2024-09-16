import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import google.generativeai as genai
import io

# Ensure the API key is configured
genai.configure(api_key="AIzaSyCcNOie26_Mm7npTI-rGBBbywfTeAal5eQ")
model = genai.GenerativeModel('gemini-1.5-flash')

class TrashClassificationModel:
    def __init__(self):
        self.input_prompt = """
            You are an expert in identifying types of trash. 
            You will receive an image as input, and your task is to classify it into one of the following categories: 
            food, plastic, glass, metal, paper, organic, medical, nuclear waste. If it's not trash, return "Not Trash".
            """

    # Function to get the response for image input
    def get_gemini_response_image(self, image, prompt):
        response = model.generate_content([image[0], prompt])
        return response.text

    # Function to set up image data for processing
    def input_image_setup(self, uploaded_image):
        if uploaded_image is not None:
            img_byte_arr = io.BytesIO()
            uploaded_image.save(img_byte_arr, format=uploaded_image.format)
            img_byte_arr = img_byte_arr.getvalue()
            image_parts = [{"mime_type": "image/jpeg", "data": img_byte_arr}]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")

    def classify_trash(self, uploaded_image):
        image_data = self.input_image_setup(uploaded_image)
        response = self.get_gemini_response_image(image_data, self.input_prompt)
        return response


class TrashClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trash Classification Tool")
        self.root.geometry("600x600")

        # Create a label for displaying the image
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        # Button to upload image
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Label to show classification result
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.uploaded_image = None
        self.trash_model = TrashClassificationModel()

    def upload_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])

        if file_path:
            # Open and display the selected image
            self.uploaded_image = Image.open(file_path)
            img_resized = self.uploaded_image.resize((300, 300))  # Resize for display
            img = ImageTk.PhotoImage(img_resized)

            self.image_label.configure(image=img)
            self.image_label.image = img

            # Classify the uploaded image
            self.classify_trash()

    def classify_trash(self):
        try:
            classification_result = self.trash_model.classify_trash(self.uploaded_image)
            self.result_label.config(text=f"Classification Result: {classification_result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = TrashClassifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
