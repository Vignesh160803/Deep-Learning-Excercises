import socket
import io
from PIL import Image
import google.generativeai as genai

# Ensure the API key is configured
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# Network settings
server_ip = "192.168.4.2"  # Raspberry Pi IP address in ESP32's network
server_port = 5000

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print(f"Listening on {server_ip}:{server_port}")

class TrashClassificationModel:
    def __init__(self):
        self.input_prompt = """
            You are an expert in identifying types of trash. 
            You will receive an image as input, and your task is to classify it into one of the following categories: 
            food, plastic, glass, metal, paper, organic, medical, nuclear waste. If it's not trash, return "Not Trash".
            """

    def classify_image(self, uploaded_image):
        # Convert the image to byte array for the API
        img_byte_arr = io.BytesIO()
        uploaded_image.save(img_byte_arr, format=uploaded_image.format)
        img_byte_arr = img_byte_arr.getvalue()

        # Send image to Gemini API
        image_parts = [{"mime_type": "image/jpeg", "data": img_byte_arr}]
        response = model.generate_content([image_parts[0], self.input_prompt])
        return response.text

def receive_image(client_socket):
    # First, receive the image size
    size_data = client_socket.recv(4)
    image_size = int.from_bytes(size_data, byteorder='big')

    # Then, receive the actual image data
    image_data = b""
    while len(image_data) < image_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        image_data += chunk

    # Convert image data to PIL Image
    img = Image.open(io.BytesIO(image_data))
    return img

def main():
    trash_model = TrashClassificationModel()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        try:
            # Receive image from ESP32-CAM
            image = receive_image(client_socket)
            print("Image received")

            # Classify the image using Gemini API
            classification_result = trash_model.classify_image(image)
            print(f"Classification Result: {classification_result}")

            # Send the classification result back to ESP32-CAM
            client_socket.sendall(classification_result.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
