from PIL import Image
import requests
import numpy as np


url = "https://i.pinimg.com/originals/1f/4a/ef/1f4aefcfdf27fe7c3ec500eae03927da.png"
image = Image.open(requests.get(url, stream=True).raw)

import sentence_transformers
from sentence_transformers import SentenceTransformer, util

#Load CLIP model
image_model = SentenceTransformer('clip-ViT-B-32')
text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
text_emb = text_model.encode(["hahaha funny smile"] )
image_emb = image_model.encode([image])
print(text_emb )
print(image_emb)
similarity = util.cos_sim(text_emb, image_emb)

print(similarity )
