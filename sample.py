import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base") 
raw_image = Image.open("TRAIN/O/O_3.jpg").convert('RGB')
text = """
            You are an expert in identifying types of trash. 
            You will receive an image as input, and your task is to classify it into one of the following categories: 
            food, plastic, glass, metal, paper, organic, medical, nuclear waste. If it's not trash, return "Not Trash".
            return only the class label
            """
inputs = processor(raw_image, text, return_tensors="pt")
import time

# Measure the time taken for conditional image captioning
start_time = time.time()
out = model.generate(**inputs, max_new_tokens=64)
print(processor.decode(out[0], skip_special_tokens=True))
end_time = time.time()
print(f"Time taken for conditional image captioning: {end_time - start_time} seconds")

# Measure the time taken for unconditional image captioning
start_time = time.time()
inputs = processor(raw_image, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=64)
end_time = time.time()
print(f"Time taken for unconditional image captioning: {end_time - start_time} seconds")

print(processor.decode(out[0], skip_special_tokens=True))
