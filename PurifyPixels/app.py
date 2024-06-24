from flask import Flask, request, jsonify, send_file
import os

from PIL import Image
import io
from .eliminate.infer import purify_image

app = Flask(__name__)

@app.route('/purify', methods=['POST'])
def purify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    img_path = os.path.join('/tmp', image_file.filename)
    image_file.save(img_path)

    purified_image, _ = purify_image(img_path)

    img = Image.fromarray(purified_image)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)