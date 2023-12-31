# -*- coding: utf-8 -*-
"""Image-Caption-Generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XBJZhLSxQWlc2-82yHOPaIKBz0C0WAij

##Image Caption Generator using hugging face models!
Image caption generator is a popular Artificial Intelligence research area that focuses on image understanding and language description. It requires syntactic and semantic understanding of language to accurately describe image content. This challenging task could help visually impaired people understand images, but is harder than image classification or object recognition tasks.
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install transformers

from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

##https://huggingface.co/nlpconnect/vit-gpt2-image-captioning
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(image_paths):
  images = []
  for image_path in image_paths:
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  return preds

predict_step(['/content/Rahul.jpeg'])

predict_step(['/content/drive/MyDrive/Personal Projects 2023/Image Caption Generator using Deep Learnings/Flickr8k_Dataset/Flicker8k_Dataset/10815824_2997e03d76.jpg'])

