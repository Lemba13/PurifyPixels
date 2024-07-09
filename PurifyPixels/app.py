from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import os

from PIL import Image
import io
from .eliminate.infer import purify_image

app = FastAPI()

@app.post("/purify")
async def purify(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image file provided")

    img_path = os.path.join('/tmp', image.filename)
    
    with open(img_path, "wb") as buffer:
        buffer.write(await image.read())

    purified_image, _ = purify_image(img_path)

    img = Image.fromarray(purified_image)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
