# PurifyPixels

## Overview
PurifyPixels is an application that detects for any steganogrphic content in images and removes the steganographic content from images using a pre-trained generative model.

## Setting Up the Environment

### Prerequisites
- Python 3.9 or higher
- Flask
- Docker 

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Lemba13/PurifyPixels.git
   cd PurifyPixels
   ```
2. Install the required dependencies:
    ```bash
    python -m pip install -r requirements.txt
    python -m pip install --no-cache-dir torch==2.3.0 --index-url https://download.pytorch.org/whl/cu121
    ```
3. Installing as a package (optional):
    ```bash
    python -m pip install -e .
    ```

### Running the application
```python
python -m PurifyPixels.app
```

The application will be available at http://127.0.0.1:5000.

### Docker stuff
1. Building the docker
    ```bash
    docker build -t purifypixel .
    ```
2. Running the container
    ```bash
    docker run --gpus all -p 5000:5000 purifypixel
    ```

### API Usage
**Purify Image
Endpoint:** /purify

Method: POST

Request
* Form-data with key `image` and the image file to be purified.

Response
* The purified image in PNG format.


**Detect Steganography
Endpoint:** /detect

Method: POST

Request
* Form-data with key `image` and the image file to be detected.

Response
* Text response of the class the image belongs to.


1. Example with curl
    ```bash
    curl -X POST -F "image=@path/to/your/image.jpg" http://127.0.0.1:5000/purify --output purified_image.png
    ```

    ```bash
    curl -X POST -F "image=@path/to/your/image.jpg" http://127.0.0.1:5000/detect
    ```

2. Example with python
    ```python
    import requests

    url = 'http://127.0.0.1:5000/purify'
    image_path = 'path/to/your/image.jpg'

    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        with open('purified_image.png', 'wb') as out_file:
            out_file.write(response.content)
        print("Purified image saved as purified_image.png")
    else:
        print(f"Failed to purify image. Status code: {response.status_code}")

    ```

3. Example with postman
    1. Open Postman and create a new POST request.
    2. Set the request URL to http://127.0.0.1:5000/purify or http://127.0.0.1:5000/purify
    3. In the "Body" tab, select "form-data".
    4. Add a new key with the name image, set the type to "File", and choose the image file you want to upload.
    5. Click "Send".
    6. The response should contain the purified image (or the detection result). You can save this image from the response.

### LICENSE
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## TODO
- [x] Update the installation instructions.
- [ ] Add usage examples.
- [x] Add a detection model
- [ ] Integrate a database for storing images (maybe).
- [ ] Implement API authentication mechanisms. (@Bong)
- [ ] Internet (@Bong)
