import cv2
import numpy as np
import os
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

# Utility function to check image clarity
def check_clarity(image_path, clarity_threshold=1000):
    """
    Check the clarity of an image using the variance of the Laplacian.

    Args:
        image_path (str): Path to the image file.
        clarity_threshold (float): Threshold for clarity assessment.

    Returns:
        str: 'Blurry' or 'Clear' based on the variance value.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return "Error: Unable to read image"

    # Compute the Laplacian and its variance
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    variance = laplacian.var()

    return "Blurry" if variance < clarity_threshold else "Clear"

# API endpoint to check clarity
@app.route('/check-clarity', methods=['POST'])
def clarity_check():
    """
    Endpoint to evaluate the clarity of an uploaded image.

    Expects:
        - Multipart/form-data with 'image_data' key containing the image file.

    Returns:
        JSON response with clarity status.
    """
    if 'image_data' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image_data']

    # Use a secure temporary file to store the image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file_path = temp_file.name
        image_file.save(temp_file_path)

    try:
        clarity = check_clarity(temp_file_path)
        return jsonify({'clarity_status': clarity})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Ensure temporary file is deleted
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == '__main__':
    app.run(debug=True)
