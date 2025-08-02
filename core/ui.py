import streamlit as st
from PIL import Image
import os

from core import core  # to call core.resize_image

def reset_state_on_new_file(uploaded_file):
    if 'uploaded_file_old' not in st.session_state:
        st.session_state.uploaded_file_old = None
    if uploaded_file != st.session_state.uploaded_file_old:
        st.session_state.uploaded_file_old = uploaded_file
        for key in ['width_val', 'resized_image_buf']:
            if key in st.session_state:
                del st.session_state[key]

def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    keys = list(st.session_state.keys())
    for key in keys:
        if key != 'uploaded_file_old':
            del st.session_state[key]

def width_selector(image_width: int):
    if 'width_val' not in st.session_state:
        st.session_state.width_val = image_width
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        slider_width = st.slider("Width (pixels)", min_value=10, max_value=image_width,
                                 value=st.session_state.width_val, step=1, key="slider_width")
    with col2:
        num_width = st.number_input(" ", min_value=10, max_value=image_width,
                                    value=st.session_state.width_val, step=1,
                                    key="num_width", label_visibility="collapsed")
    if slider_width != st.session_state.width_val:
        st.session_state.width_val = slider_width
    elif num_width != st.session_state.width_val:
        st.session_state.width_val = num_width
    return st.session_state.width_val

def jpeg_quality_selector(default_quality: int = 95):
    st.sidebar.header("Quality (JPEG only)")
    quality = st.sidebar.slider("JPEG Quality", min_value=10, max_value=95,
                                value=default_quality, step=1,
                                help="Higher quality = larger file size")
    return quality

def download_button(data: bytes, filename: str, mime: str):
    st.sidebar.download_button(
        label="Download Resized Image",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True
    )

def run_streamlit_app():
    st.set_page_config(page_title="Image Resizer with Quality Control", layout="centered")
    st.title("Image Resizer with Editable Width & Quality")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    clear_cache()
    reset_state_on_new_file(uploaded_file)
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        width = width_selector(image.width)
        aspect_ratio = image.height / image.width
        height = int(width * aspect_ratio)
        quality = jpeg_quality_selector(default_quality=95)
        if st.sidebar.button("Resize Image"):
            resized_img, img_format, buf = core.resize_image(image, width, height, quality)
            file_size_bytes = len(buf.getvalue())
            if file_size_bytes >= 1024 * 1024:
                size_text = f"Estimated file size: {file_size_bytes/(1024*1024):.2f} MB"
            else:
                size_text = f"Estimated file size: {file_size_bytes/1024:.2f} KB"
            st.subheader(f"Resized Image ({width} x {height})")
            st.image(resized_img, use_container_width=True)
            st.write(size_text)
            st.session_state.resized_image_buf = buf.getvalue()
            original_name = uploaded_file.name
            name, ext = os.path.splitext(original_name)
            ext = ext.lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                ext = f".{img_format.lower()}"
            save_name = f"{name}_resized{ext}"
            download_button(data=buf.getvalue(), filename=save_name, mime=f"image/{img_format.lower()}")
