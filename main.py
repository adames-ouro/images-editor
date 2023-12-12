import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import base64
from rembg import remove
import streamlit.components.v1 as components

# dowload button
def get_image_download_link(img, filename, text, format):
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    img_str = buffered.getvalue()
    b64 = base64.b64encode(img_str).decode()
    
    # Adding inline CSS for styling with hover effect
    button_style = """
    <style>
        .download-link {
            display: inline-block;
            text-decoration: none;
            padding: 8px 16px;
            margin: 5px 0;
            color: black !important;  /* Text color, with !important for higher specificity */
            background-color: grey;
            border-radius: 8px;
            font-weight: bold;
            transition: color 0.3s;  /* Smooth transition for color change */
        }

        .download-link:hover {
            color: white !important;  /* Text color on hover, with !important for higher specificity */
        }
    </style>
    """

    href = f'{button_style}<a href="data:file/jpg;base64,{b64}" download="{filename}" class="download-link">{text}</a>'
    return href

# enhance image quality
def enhance_image_quality(img, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0, gamma=1.0, equalize_hist=False):
    # Convert to PIL for some operations
    try:
        pil_img = Image.fromarray(img)
    except:
        pil_img = img

    # Adjust brightness
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(brightness)

    # Adjust contrast
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(contrast)

    # Convert back to OpenCV
    img = np.array(pil_img)

    # Adjust saturation
    if saturation != 1.0:
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    # Adjust sharpness
    if sharpness != 1.0:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * sharpness
        img = cv2.filter2D(img, -1, kernel)

    # Gamma correction
    if gamma != 1.0:
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        img = cv2.LUT(img, table)

    # Histogram Equalization
    if equalize_hist:
        img_y_cr_cb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        img_y_cr_cb[:, :, 0] = cv2.equalizeHist(img_y_cr_cb[:, :, 0])
        img = cv2.cvtColor(img_y_cr_cb, cv2.COLOR_YCrCb2RGB)


    return img

# remove background
def background_removal_page(uploaded_file):
    # name
    st.markdown('<h4 style="color: grey;">Background Removal</h4>', unsafe_allow_html=True)
    
    # process image logic
    if uploaded_file is not None:
        # loading message
        with st.spinner('Processing image... Please wait.'):
            # open image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

            # remove filter
            output_image = remove(opencv_image)
            st.session_state.original_image = opencv_image.copy()
            st.session_state.no_background = output_image.copy()

            # Display images side by side
            col1, col2 = st.columns(2)
            col1.image(st.session_state.original_image, use_column_width=True,
                        caption="Original Image")
            
            col2.image(st.session_state.no_background, use_column_width=True,
                        caption="Image without Background")

            # Download button for the processed image
            if st.session_state.no_background is not None:
                pil_enhanced = Image.fromarray(st.session_state.no_background)
                download_link = get_image_download_link(pil_enhanced, "processed_image.jpg", "Download Backgroundless Image", "PNG")
                st.markdown(download_link, unsafe_allow_html=True)

# adjust image
def adjustment_page(uploaded_file):
    # name
    st.markdown('<h4 style="color: grey;">Image Adjustment</h4>', unsafe_allow_html=True)
    
    # process image logic
    if uploaded_file is not None:
        # loading message
        with st.spinner('Processing image... Please wait.'):
            # open image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

            st.sidebar.title("Adjustments")

            brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
            saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
            sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0)
            gamma = st.sidebar.slider("Gamma", 0.0, 2.0, 1.0)
            equalize_hist = st.sidebar.checkbox("Equalize Histogram")

            # Apply the enhancements
            enhanced_image = enhance_image_quality(opencv_image,
                                                   brightness,
                                                   contrast,
                                                   saturation,
                                                   sharpness,
                                                   gamma,
                                                   equalize_hist)
            
            st.session_state.original_image = opencv_image.copy()
            st.session_state.adjusted_image = enhanced_image.copy()

            # Display images side by side
            col1, col2 = st.columns(2)
            col1.image(st.session_state.original_image, channels="RGB", caption="Original Image")
            col2.image(st.session_state.adjusted_image, channels="RGB", caption="Enhanced Image")

            # Download button for the enhanced image
            pil_enhanced = Image.fromarray(st.session_state.adjusted_image)
            download_link = get_image_download_link(pil_enhanced, "enhanced_image.jpg", "Download Enhanced Image","PNG")
            st.markdown(download_link, unsafe_allow_html=True)

# remove background and adjust image
def background_removal_adjustment(uploaded_file):
    # name
    st.markdown('<h4 style="color: grey;">Background Removal & Image Adjustment</h4>', unsafe_allow_html=True)
    
    # process image logic
    if uploaded_file is not None:
        # loading message
        with st.spinner('Processing image... Please wait.'):
            # open image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

            # remove filter
            output_image = remove(opencv_image)
            st.session_state.original_image = opencv_image.copy()
            st.session_state.no_background = output_image.copy()

            st.sidebar.title("Adjustments")

            brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
            saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
            sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0)
            gamma = st.sidebar.slider("Gamma", 0.0, 2.0, 1.0)
            equalize_hist = st.sidebar.checkbox("Equalize Histogram")
            colored_background = st.sidebar.checkbox("Color Background")
            image_background = st.sidebar.checkbox("Image Background")

            # Apply the enhancements
            enhanced_image = enhance_image_quality(st.session_state.no_background,
                                                brightness,
                                                contrast,
                                                saturation,
                                                sharpness,
                                                gamma,
                                                equalize_hist)
                
            st.session_state.adjusted_image = enhanced_image.copy()

            if colored_background == True:
                image_background = False
                color_code = st.color_picker('Pick a Color', '#00f900')
                rgb_color = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
                height, width, channels = opencv_image.shape
                original_size = (width, height)
                background = Image.new('RGB', original_size, rgb_color)
                background.paste(Image.fromarray(enhanced_image), (0, 0), Image.fromarray(enhanced_image) if Image.fromarray(enhanced_image).mode == 'RGBA' else None)
                st.session_state.adjusted_image = background.copy()

            if image_background == True:
                colored_background = False
                background = st.file_uploader('Choose a background image...',
                                type=["jpg", "png", "jpeg"])
                if background is not None:
                    file_bytes2 = np.asarray(bytearray(background.read()), dtype=np.uint8)
                    background_image = cv2.imdecode(file_bytes2, 1)
                    background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
                    b_height, b_width, _ = background_image.shape
                    height, width, channels = opencv_image.shape
                    background_image = Image.fromarray(background_image)
                    if (b_height != height) or (b_width != width):
                        background_image = background_image.resize((int(width), int(height)), Image.LANCZOS)
                    background_image.paste(Image.fromarray(enhanced_image), (0, 0), Image.fromarray(enhanced_image) if Image.fromarray(enhanced_image).mode == 'RGBA' else None)
                    st.session_state.adjusted_image = background_image.copy()

            # Display images side by side
            col1, col2, col3 = st.columns(3)
            col1.image(st.session_state.original_image, channels="RGB", caption="Original Image")
            col2.image(st.session_state.no_background, channels="RGB", caption="No Background Image")
            col3.image(st.session_state.adjusted_image, channels="RGB", caption="Enhanced Image")

            # Download button for the processed image
            if st.session_state.adjusted_image is not None:
                try:
                    pil_enhanced = Image.fromarray(st.session_state.adjusted_image)
                except:
                    pil_enhanced = st.session_state.adjusted_image
                download_link = get_image_download_link(pil_enhanced, "enhanced_image.jpg", "Download Enhanced Image", "PNG")
                st.markdown(download_link, unsafe_allow_html=True)

# Navigation
st.title('Image Enhancement')
st.markdown('<h6 style="color: white;">High quality image editing. After uploading image, check boxes for desired actions.</h6>', unsafe_allow_html=True)
st.markdown('<h6 style="color: white;">Upload images as: jpg, png or jpeg extensions.</h6>', unsafe_allow_html=True)

# upload image
uploaded_file = st.file_uploader('Choose an image...',
                                type=["jpg", "png", "jpeg"])

# Optios
background_removal = st.checkbox('Remove background')
image_adjust = st.checkbox('Adjust image')

# remove background condition
if (background_removal == True) and (image_adjust == False):
    background_removal_page(uploaded_file)

# adjust image condition
elif (background_removal == False) and (image_adjust == True):
    adjustment_page(uploaded_file)

# adjust image condition
elif (background_removal == True) and (image_adjust == True):
    background_removal_adjustment(uploaded_file)

# No selection
elif (background_removal == False) and (image_adjust == False) and (uploaded_file is None):
    image = Image.open('./images/amelie_agoldenretriever.jpg')
    
    # remove filter
    output_image = remove(image)

    st.sidebar.title("Adjustments")
    brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 0.82)
    contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0)
    saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0)
    sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0)
    gamma = st.sidebar.slider("Gamma", 0.0, 2.0, 1.29)
    equalize_hist = st.sidebar.checkbox("Equalize Histogram",value=True)

    # Apply the enhancements
    enhanced_image = enhance_image_quality(image, brightness, contrast, saturation, sharpness, gamma, equalize_hist)
    
    # Display images side by side
    col1, col2, col3 = st.columns(3)
    col1.image(image, channels="RGB", caption="Original Image")
    col2.image(output_image, channels="RGB", caption="No Background Image")
    col3.image(enhanced_image, channels="RGB", caption="Enhanced Image")
    st.write(f'Shoutout to the amazing model, Amelie  🐾')
    instagram_embed_code = '''<blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/amelie_agoldenretriever/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:16px;"> <a href="https://www.instagram.com/amelie_agoldenretriever/?utm_source=ig_embed&amp;utm_campaign=loading" style=" background:#FFFFFF; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank"> <div style=" display: flex; flex-direction: row; align-items: center;"> <div style="background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 40px; margin-right: 14px; width: 40px;"></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 100px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 60px;"></div></div></div><div style="padding: 19% 0;"></div> <div style="display:block; height:50px; margin:0 auto 12px; width:50px;"><svg width="50px" height="50px" viewBox="0 0 60 60" version="1.1" xmlns="https://www.w3.org/2000/svg" xmlns:xlink="https://www.w3.org/1999/xlink"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-511.000000, -20.000000)" fill="#000000"><g><path d="M556.869,30.41 C554.814,30.41 553.148,32.076 553.148,34.131 C553.148,36.186 554.814,37.852 556.869,37.852 C558.924,37.852 560.59,36.186 560.59,34.131 C560.59,32.076 558.924,30.41 556.869,30.41 M541,60.657 C535.114,60.657 530.342,55.887 530.342,50 C530.342,44.114 535.114,39.342 541,39.342 C546.887,39.342 551.658,44.114 551.658,50 C551.658,55.887 546.887,60.657 541,60.657 M541,33.886 C532.1,33.886 524.886,41.1 524.886,50 C524.886,58.899 532.1,66.113 541,66.113 C549.9,66.113 557.115,58.899 557.115,50 C557.115,41.1 549.9,33.886 541,33.886 M565.378,62.101 C565.244,65.022 564.756,66.606 564.346,67.663 C563.803,69.06 563.154,70.057 562.106,71.106 C561.058,72.155 560.06,72.803 558.662,73.347 C557.607,73.757 556.021,74.244 553.102,74.378 C549.944,74.521 548.997,74.552 541,74.552 C533.003,74.552 532.056,74.521 528.898,74.378 C525.979,74.244 524.393,73.757 523.338,73.347 C521.94,72.803 520.942,72.155 519.894,71.106 C518.846,70.057 518.197,69.06 517.654,67.663 C517.244,66.606 516.755,65.022 516.623,62.101 C516.479,58.943 516.448,57.996 516.448,50 C516.448,42.003 516.479,41.056 516.623,37.899 C516.755,34.978 517.244,33.391 517.654,32.338 C518.197,30.938 518.846,29.942 519.894,28.894 C520.942,27.846 521.94,27.196 523.338,26.654 C524.393,26.244 525.979,25.756 528.898,25.623 C532.057,25.479 533.004,25.448 541,25.448 C548.997,25.448 549.943,25.479 553.102,25.623 C556.021,25.756 557.607,26.244 558.662,26.654 C560.06,27.196 561.058,27.846 562.106,28.894 C563.154,29.942 563.803,30.938 564.346,32.338 C564.756,33.391 565.244,34.978 565.378,37.899 C565.522,41.056 565.552,42.003 565.552,50 C565.552,57.996 565.522,58.943 565.378,62.101 M570.82,37.631 C570.674,34.438 570.167,32.258 569.425,30.349 C568.659,28.377 567.633,26.702 565.965,25.035 C564.297,23.368 562.623,22.342 560.652,21.575 C558.743,20.834 556.562,20.326 553.369,20.18 C550.169,20.033 549.148,20 541,20 C532.853,20 531.831,20.033 528.631,20.18 C525.438,20.326 523.257,20.834 521.349,21.575 C519.376,22.342 517.703,23.368 516.035,25.035 C514.368,26.702 513.342,28.377 512.574,30.349 C511.834,32.258 511.326,34.438 511.181,37.631 C511.035,40.831 511,41.851 511,50 C511,58.147 511.035,59.17 511.181,62.369 C511.326,65.562 511.834,67.743 512.574,69.651 C513.342,71.625 514.368,73.296 516.035,74.965 C517.703,76.634 519.376,77.658 521.349,78.425 C523.257,79.167 525.438,79.673 528.631,79.82 C531.831,79.965 532.853,80.001 541,80.001 C549.148,80.001 550.169,79.965 553.369,79.82 C556.562,79.673 558.743,79.167 560.652,78.425 C562.623,77.658 564.297,76.634 565.965,74.965 C567.633,73.296 568.659,71.625 569.425,69.651 C570.167,67.743 570.674,65.562 570.82,62.369 C570.966,59.17 571,58.147 571,50 C571,41.851 570.966,40.831 570.82,37.631"></path></g></g></g></svg></div><div style="padding-top: 8px;"> <div style=" color:#3897f0; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:550; line-height:18px;">View this profile on Instagram</div></div><div style="padding: 12.5% 0;"></div> <div style="display: flex; flex-direction: row; margin-bottom: 14px; align-items: center;"><div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(0px) translateY(7px);"></div> <div style="background-color: #F4F4F4; height: 12.5px; transform: rotate(-45deg) translateX(3px) translateY(1px); width: 12.5px; flex-grow: 0; margin-right: 14px; margin-left: 2px;"></div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(9px) translateY(-18px);"></div></div><div style="margin-left: 8px;"> <div style=" background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 20px; width: 20px;"></div> <div style=" width: 0; height: 0; border-top: 2px solid transparent; border-left: 6px solid #f4f4f4; border-bottom: 2px solid transparent; transform: translateX(16px) translateY(-4px) rotate(30deg)"></div></div><div style="margin-left: auto;"> <div style=" width: 0px; border-top: 8px solid #F4F4F4; border-right: 8px solid transparent; transform: translateY(16px);"></div> <div style=" background-color: #F4F4F4; flex-grow: 0; height: 12px; width: 16px; transform: translateY(-4px);"></div> <div style=" width: 0; height: 0; border-top: 8px solid #F4F4F4; border-left: 8px solid transparent; transform: translateY(-4px) translateX(8px);"></div></div></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center; margin-bottom: 24px;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 224px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 144px;"></div></div></a><p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://www.instagram.com/amelie_agoldenretriever/?utm_source=ig_embed&amp;utm_campaign=loading" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px;" target="_blank">Amélie</a> (@<a href="https://www.instagram.com/amelie_agoldenretriever/?utm_source=ig_embed&amp;utm_campaign=loading" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px;" target="_blank">amelie_agoldenretriever</a>) • Instagram photos and videos</p></div></blockquote> <script async src="//www.instagram.com/embed.js"></script>'''
    components.html(instagram_embed_code,width=600,height=600)
