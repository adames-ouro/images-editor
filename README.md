
# Image Enhancement Streamlit App

This Streamlit application offers a range of image processing functionalities, including background removal, image adjustment, and image enhancement.

## Features

1. **Background Removal**: Remove the background from images.
2. **Image Adjustment**: Adjust brightness, contrast, saturation, sharpness, and gamma of images.
3. **Enhance Image Quality**: Enhance the overall quality of images.

## How to Use

1. **Upload an Image**: Select an image with `.jpg`, `.png`, or `.jpeg` extensions.
2. **Choose Processing Options**:
   - Check 'Remove background' to remove the image background.
   - Check 'Adjust image' to adjust image parameters.
3. **Download Processed Images**: Use the generated download link to save the enhanced images.

### Background Removal Page

This page allows users to upload an image and remove its background. The original and processed images are displayed side by side. 

```python
def background_removal_page(uploaded_file):
    # Function implementation...
```

### Image Adjustment Page

Users can adjust various properties like brightness, contrast, etc., of their uploaded image. Both original and adjusted images are displayed for comparison.

```python
def adjustment_page(uploaded_file):
    # Function implementation...
```

### Combined Background Removal and Adjustment

This function combines both background removal and image adjustment functionalities.

```python
def background_removal_adjustment(uploaded_file):
    # Function implementation...
```

## Installation

To run this app, you need to install the required libraries:

```bash
pip install streamlit cv2 numpy Pillow rembg
```

## Running the App

Execute the following command to run the app:

```bash
streamlit run your_script_name.py
```

## Example Output

An example showcasing the app's functionality with a sample image.

![Original Image](link-to-original-image)
![Processed Image](link-to-processed-image)

## Dependencies

- Streamlit
- OpenCV
- NumPy
- Pillow
- REmbg

## Author

Developed by [Your Name or GitHub Username]

## License

This project is licensed under the [MIT License](LICENSE.md).
