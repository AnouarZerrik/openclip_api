import requests
from pathlib import Path
import json

def test_text_embedding(api_url, texts):
    """Tests the /embed/text endpoint."""
    url = f"{api_url}/embed/text"
    headers = {"Content-Type": "application/json"}
    data = {"texts": texts}

    try:
      response = requests.post(url, headers=headers, json=data)
      response.raise_for_status()
      print("Text embedding successful!")
      print("Response:", response.json())

    except requests.exceptions.RequestException as e:
      print(f"Error during text embedding: {e}")


def test_image_embedding_uris(api_url, image_uris):
  """Tests the /embed/image endpoint using URIs."""
  url = f"{api_url}/embed/image"
  headers = {"Content-Type": "application/json"}
  data = {"image_uris": image_uris}
  try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("Image embedding using URIs successful!")
    print("Response:", response.json())
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error during image embedding using URIs: {e}")


def test_image_upload_endpoint(api_url, image_paths):
    """Tests the /embed/image-upload endpoint by sending image files as multipart form data."""
    url = f"{api_url}/embed/image-upload"

    try:
        files = []
        for image_path in image_paths:
          if not Path(image_path).is_file():
            raise FileNotFoundError(f"Image file not found {image_path}")
          files.append(("images", open(image_path, "rb")))

        response = requests.post(url, files=files)
        response.raise_for_status()
        print("Image upload successful!")
        print("Response:", response.json())
        return response.json()

    except FileNotFoundError as e:
      print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error during image upload: {e}")
    finally:
      # Close files
      if 'files' in locals():
        for name, file in files:
          file.close()

def test_health_check(api_url):
  """Tests the /health endpoint."""
  url = f"{api_url}/health"
  try:
    response = requests.get(url)
    response.raise_for_status()
    print("Health check successful!")
    print("Response:", response.json())
  except requests.exceptions.RequestException as e:
    print(f"Error during health check: {e}")

def find_image_paths_in_directory(directory_path, extensions=(".jpg", ".jpeg", ".png", ".gif")):
    """
    Finds all image files with specified extensions in a given directory.

    Args:
        directory_path (str): The path to the directory.
        extensions (tuple): A tuple of valid image file extensions.

    Returns:
        List[str]: A list of absolute paths to the image files.
    """
    directory = Path(directory_path)
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    image_paths = []
    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() in extensions:
            image_paths.append(str(item.resolve()))  # Store absolute path
    return image_paths

if __name__ == "__main__":
    api_url = "http://localhost:8001"  # Replace with your API URL if different

    directory_path = "C:/Users/UTENTE/Desktop/Projects/openclip_api/imgs"  # Replace with the actual directory path
    try:
        image_paths = find_image_paths_in_directory(directory_path)
        if image_paths:
            print("Image paths found:")
            for path in image_paths:
                print(path)
        else:
            print("No image files found in the directory.")
    except FileNotFoundError as e:
        print(e)








    # Test Text Embedding
    # texts = ["Hello", "World"]
    # test_text_embedding(api_url, texts)

    # Test Image Embedding with URIs
    # image_uris = [
    #     "/images_host/team.png"
    # ]  # Add your image urls
    # data = test_image_embedding_uris(api_url, image_uris)

    # Test Image Upload
    # image_paths = [
    #     "C:/Users/UTENTE/Desktop/Projects/openclip_api/imgs/team.png"
    # ]
    data = test_image_upload_endpoint(api_url, image_paths)
    print("---------------------------")
    print(len(data['embeddings']))
    
    # data = json.loads(data)
    
    # print(len(data['embeddings']))
    
    # # Test Health check
    # test_health_check(api_url)