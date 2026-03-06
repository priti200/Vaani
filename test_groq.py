# test_groq.py

import os
from dotenv import load_dotenv
from services.groq import ask_groq

load_dotenv()

# Simulate a small piece of "PDF text"
fake_pdf = """
This paper presents a new deep learning model called VisionNet.
VisionNet uses a transformer architecture with 12 layers.
It was trained on ImageNet dataset with 1.2 million images.
The model achieves 94.5% accuracy on image classification tasks.
The training took 3 days on 8 A100 GPUs.
"""

question = "What accuracy does VisionNet achieve?"

print("Asking Groq...")
answer = ask_groq(question, fake_pdf, "en-IN")
print(f"\nQuestion: {question}")
print(f"Answer: {answer}")