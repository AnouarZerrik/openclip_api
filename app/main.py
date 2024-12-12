from typing import List, Dict
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import tempfile
import uuid
import os
from openclip_utils import load_openclip_model, embed_text, embed_image
import torch

app = FastAPI()

# Configurations for model
MODEL_NAME = "ViT-B-32"
CHECKPOINT = "laion2b_s34b_b79k"

# Volume for caching the model
MODEL_CACHE_DIR = "/model_cache"

# Path inside container that mount the images of the host
IMAGE_VOLUME_PATH = "/images_host"

# Check if the model is cached
def load_cached_model():
    model_path = Path(MODEL_CACHE_DIR) / f"{MODEL_NAME}_{CHECKPOINT}.pt"
    if model_path.is_file():
      try:
         print(f"Loading cached model from: {model_path}")
         model_obj = torch.load(model_path)
         return model_obj
      except Exception as e:
          print(f"Error loading cached model, loading model from start {e}")
          return None
    else:
        print("No cached model found, loading from scratch")
        return None


# Load the OpenCLIP model on startup
clip_model = load_cached_model()
if clip_model is None:
    try:
      clip_model = load_openclip_model(MODEL_NAME, CHECKPOINT)
      # Save the model to the cache
      os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
      model_path = Path(MODEL_CACHE_DIR) / f"{MODEL_NAME}_{CHECKPOINT}.pt"
      torch.save(clip_model, model_path)
      print(f"Model cached to: {model_path}")
    except Exception as e:
        raise Exception(f"Failed to load or cache OpenCLIP model: {e}")


class TextEmbeddingRequest(BaseModel):
    texts: List[str]

class TextEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

class ImageEmbeddingRequest(BaseModel):
    image_uris: List[str]

class ImageEmbeddingResponse(BaseModel):
   embeddings: List[List[float]]

class HealthResponse(BaseModel):
  status: str


@app.post("/embed/text", response_model=TextEmbeddingResponse)
async def embed_text_endpoint(request: TextEmbeddingRequest):
    try:
        embeddings = embed_text(clip_model, request.texts)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding text: {e}")


@app.post("/embed/image", response_model=ImageEmbeddingResponse)
async def embed_image_endpoint(request: ImageEmbeddingRequest):
    try:
        embeddings = embed_image(clip_model, request.image_uris)
        return {"embeddings": embeddings}
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error embedding image: {e}")

@app.post("/embed/image-upload", response_model=ImageEmbeddingResponse)
async def embed_image_upload_endpoint(images: List[UploadFile] = File(...)):
    try:
        image_uris = []
        for image in images:
          try:
             temp_file_path = Path(tempfile.gettempdir()) / f"{uuid.uuid4()}-{image.filename}"
             with open(temp_file_path, "wb") as buffer:
              buffer.write(await image.read())
              image_uris.append(str(temp_file_path))
          except Exception as e:
              raise HTTPException(status_code=500, detail=f"Error processing image: {e}")
        embeddings = embed_image(clip_model, image_uris)
        # Clean up temporary files
        for uri in image_uris:
         Path(uri).unlink(missing_ok=True)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding image: {e}")

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)