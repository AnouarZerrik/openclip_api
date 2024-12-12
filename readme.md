Okay, let's create a simplified README that focuses on running the API with Docker and sending requests, without delving into Java testing. We'll keep it concise and easy to follow.

```markdown
# OpenCLIP FastAPI API with Docker

This repository contains a FastAPI application that uses the OpenCLIP model for generating text and image embeddings. The application is containerized using Docker for easy deployment.

## Prerequisites

Before getting started, make sure you have the following installed:

*   [Docker](https://www.docker.com/get-started)
*   [curl](https://curl.se/download.html) or a similar command-line tool for sending HTTP requests

## Running the API with Docker

### 1. Build the Docker Image

Navigate to the root directory of the repository and run the following command to build the Docker image:

```bash
docker build -t openclip-api .
```

### 2. Run the Docker Container

To run the Docker container, use the following command:

```bash
docker run -p 8000:8000 \
    -v /path/on/host/model_cache:/model_cache \
    -v /path/on/host/images:/images_host \
    openclip-api
```

Replace `/path/on/host/model_cache` and `/path/on/host/images` with the actual paths to directories on your host machine.

*   **`-p 8000:8000`**: Maps port 8000 on your host to port 8000 in the container.
*   **`-v /path/on/host/model_cache:/model_cache`**: Creates a volume mount for caching the OpenCLIP model. This prevents the model from being downloaded every time the container restarts.
*   **`-v /path/on/host/images:/images_host`**: Creates a volume mount for accessing images on the host machine from within the container.
*   **`openclip-api`**: The name of the Docker image you built earlier.

## API Endpoints and How to Send Requests

The API provides the following endpoints:

### 1. `/embed/text`

**Description:** Generates embeddings for text.
**Method:** `POST`
**Request Body:** JSON with the following structure:
   ```json
   {
     "texts": ["text1", "text2", ...]
   }
   ```
**Response Body:** JSON with the following structure:
    ```json
    {
      "embeddings": [
          [0.1, 0.2, 0.3, ...],
          [0.4, 0.5, 0.6, ...],
          ...
      ]
     }
    ```
**Example using `curl`:**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"texts": ["dog", "cat"]}' http://localhost:8000/embed/text
   ```

### 2. `/embed/image`

**Description:** Generates embeddings for images using URIs.
**Method:** `POST`
**Request Body:** JSON with the following structure:

   ```json
   {
     "image_uris": ["image_url1", "image_path2", ...]
   }
   ```

  * The `image_uris` can be a URL (`http://` or `https://`) or a file path in the local filesystem.
  * When using the file path, remember to use the `/images_host` path inside the container to access your local files, as defined in the volume mount.
**Response Body:** JSON with the following structure:
    ```json
    {
      "embeddings": [
          [0.1, 0.2, 0.3, ...],
          [0.4, 0.5, 0.6, ...],
          ...
      ]
     }
    ```

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image_uris": ["/images_host/your_image_1.png", "/images_host/your_image_1.png"]}' http://localhost:8000/embed/image
```

*   **Remember to replace `your_image.png` with an actual image name inside your mounted directory `/path/on/host/images`**

### 3. `/embed/image-upload`

**Description:** Generates embeddings for images by uploading image files.
**Method:** `POST`
**Request Body:**  Multipart form data with the images as files, with a form field named `images`.
**Response Body:** JSON with the following structure:
    ```json
    {
      "embeddings": [
          [0.1, 0.2, 0.3, ...],
          [0.4, 0.5, 0.6, ...],
          ...
      ]
     }
    ```
**Example using `curl`:**

```bash
curl -X POST -F "images=@/path/to/your/image1.jpg" -F "images=@/path/to/your/image2.png" http://localhost:8000/embed/image-upload
```

*   Replace `/path/to/your/image1.jpg` and `/path/to/your/image2.png` with the paths to your image files.

### 4. `/health`

**Description:** Returns the health of the API.
**Method:** `GET`
**Response Body:** JSON with the following structure:
    ```json
    {
        "status": "ok"
    }
   ```
**Example using `curl`:**

```bash
curl http://localhost:8000/health
```

## Important Notes

*   **Volume Mounts**: Remember to use the volume mounts to cache the model and provide access to your images.
*   **Image Paths**: When using the `/embed/image` endpoint with local file paths, make sure the paths are accessible inside the Docker container (e.g., `/images_host/your_image.jpg`).
*   **Environment**:  The docker container does not require environment variables.
*   **CPU only**: This image was built using pytorch CPU only, so you cannot use CUDA acceleration.

## Additional Information

*   The OpenCLIP model will be cached in the `/model_cache` directory within the container. This directory is persisted through the volume mount.
*   If you modify the code in the `app` directory, you'll need to rebuild the Docker image.

This README provides you with the basic information you need to run the API with Docker and send requests. The Python test script is included only if you wish to do some development to the code.


**Key Changes in this Simplified README:**

*   **Focus on `curl`:**  It primarily uses `curl` examples for sending requests, which is simpler than explaining the Python testing script in detail.
*   **No Java testing:**  The Java test files are removed from the explanation.
*   **Concise and direct:** The language is more straightforward, focusing on how to run the API and send requests to it.
*  **Simplified Structure**: The explanation for the test script is removed, keeping the project focused on the running and using the API with Docker.

This simplified README will be more user-friendly for users who just want to quickly run the API and interact with it. The Python testing is still included in case the user want to explore the code, or use it as a example for testing.
