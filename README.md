
# Image Enhancement and Background Removal App

![Image_Processing_App](./images/amelie_agoldenretriever.jpg)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Acknowledgements](#acknowledgements)

## Overview

This Streamlit-based application offers advanced image processing capabilities, including high-quality image enhancement and background removal. It provides users with intuitive tools for improving image quality and customizing their photos with ease.

## Features
1. **Background Removal**: Efficiently removes the background from images, leaving the subject intact.
2. **Image Quality Enhancement**: Adjusts parameters like brightness, contrast, and sharpness to improve overall image quality.
3. **Interactive User Interface**: Easy-to-use sliders and checkboxes for adjusting image parameters.
4. **Real-time Image Processing**: Quickly processes images and displays results in real time.
5. **Downloadable Results**: Users can download enhanced images directly from the app.

## Requirements

- Python 3.6 or newer.
- Libraries: `streamlit`, `opencv-python`, `numpy`, `Pillow`, `rembg`.

## Installation & Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-github-username/Image-Processing-App.git
    cd Image-Processing-App
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
    streamlit run image_processing_app.py 
    ```

5. **Access the App**: Open your browser and go to `http://localhost:8501`.

## Acknowledgements

- Image processing capabilities powered by [OpenCV](https://opencv.org/).
- Background removal functionality provided by [REmbg](https://github.com/danielgatis/rembg).
- UI and app development using [Streamlit](https://www.streamlit.io/).
