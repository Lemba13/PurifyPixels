from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse
import os

from PIL import Image
import io
from .eliminate.infer import purify_image
from .detect.infer import predict_steganography
import tempfile

app = FastAPI()

# To remove steganographic content from an image
@app.post("/purify")
async def purify(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image file provided")

    # Ensure the tmp directory exists
    tmp_dir = 'tmp'
    os.makedirs(tmp_dir, exist_ok=True)

    img_path = os.path.join(tmp_dir, image.filename)
    
    # Save the uploaded image to the tmp directory
    with open(img_path, "wb") as buffer:
        buffer.write(await image.read())

    purified_image, _ = purify_image(img_path)

    img = Image.fromarray(purified_image)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")

# To detect the type of steganographic content present in the image
@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image file provided")

    # Ensure the tmp directory exists
    tmp_dir = 'tmp'
    os.makedirs(tmp_dir, exist_ok=True)

    img_path = os.path.join(tmp_dir, image.filename)
    
    # Save the uploaded image to the tmp directory
    with open(img_path, "wb") as buffer:
        buffer.write(await image.read())


    # Call predict steganography function on the image sent by the api request
    result = predict_steganography(img_path)

    return PlainTextResponse(result)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
