import open_clip
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from PIL import Image
from typing import List


def load_openclip_model(model_name: str, checkpoint: str):
    """Loads the OpenCLIP model with the given model name and checkpoint."""
    return OpenCLIPEmbeddings(model_name=model_name, checkpoint=checkpoint)


def embed_text(model: OpenCLIPEmbeddings, texts: List[str]) -> List[List[float]]:
    """Embeds a list of text strings using the OpenCLIP model."""
    return model.embed_documents(texts)


def embed_image(model: OpenCLIPEmbeddings, image_uris: List[str]) -> List[List[float]]:
    """Embeds a list of image URIs using the OpenCLIP model."""
    return model.embed_image(image_uris)


if __name__ == '__main__':
    # Example usage for testing:
    model_name = "ViT-B-32"
    checkpoint = "laion2b_s34b_b79k"
    clip_model = load_openclip_model(model_name, checkpoint)
    
    # Mock image paths (replace with actual image paths for testing)
    # create a dummy image
    from PIL import Image
    import numpy as np
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    img.save("test_image.png")
    uri_dog = "test_image.png"
    uri_house = "test_image.png"
    
    img_feat_dog = embed_image(clip_model, [uri_dog])
    img_feat_house = embed_image(clip_model, [uri_house])
    text_feat_dog = embed_text(clip_model, ["dog"])
    text_feat_house = embed_text(clip_model, ["house"])
    
    print("Image Embedding Dog: ", len(img_feat_dog[0]))
    print("Image Embedding House: ", len(img_feat_house[0]))
    print("Text Embedding Dog: ", len(text_feat_dog[0]))
    print("Text Embedding House: ", len(text_feat_house[0]))