
# Image Enhancement and Background Removal App

![Image_Processing_App](./images/example1.png)


This Streamlit-based application offers advanced image processing capabilities, including high-quality image enhancement and background removal. It provides users with intuitive tools for improving image quality and customizing their photos with ease.

## Features
1. **Background Removal**: Efficiently removes the background from images, leaving the subject intact.
2. **Image Quality Enhancement**: Adjusts parameters like brightness, contrast, and sharpness to improve overall image quality.
3. **Interactive User Interface**: Easy-to-use sliders and checkboxes for adjusting image parameters.
4. **Downloadable Results**: Users can download enhanced images directly from the app.

## Requirements

- Python 3.11 or newer.
- Libraries: `streamlit`, `opencv-python`, `numpy`, `Pillow`, `rembg`.

## Installation & Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-github-username/images-editor.git
    cd images-editor
    ```

2. **Setup a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3. **Install Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit App**:
    ```bash
    streamlit run main.py 
    ```

