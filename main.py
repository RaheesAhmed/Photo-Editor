import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter
import io

def main():
    st.title("Advanced Image Editor")

    st.sidebar.write("## Upload Image")
    uploaded_file = st.sidebar.file_uploader("", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.sidebar.image(image, caption="Uploaded Image", use_column_width=True)
        
        st.write("## Edited Image")

        # Rotation
        rotate = st.sidebar.slider("Rotate", 0, 360, step=10)
        rotated_image = image.rotate(rotate)
        
        # Brightness
        brightness = st.sidebar.slider("Brightness", 1.0, 3.0, step=0.1)
        enhancer = ImageEnhance.Brightness(rotated_image)
        brightened_image = enhancer.enhance(brightness)
        
        # Contrast
        contrast = st.sidebar.slider("Contrast", 1.0, 3.0, step=0.1)
        enhancer = ImageEnhance.Contrast(brightened_image)
        contrasted_image = enhancer.enhance(contrast)

        # Sharpness
        sharpness = st.sidebar.slider("Sharpness", 1.0, 3.0, step=0.1)
        enhancer = ImageEnhance.Sharpness(contrasted_image)
        sharpened_image = enhancer.enhance(sharpness)

        # Grayscale
        grayscale = st.sidebar.checkbox("Grayscale")
        edited_image = ImageOps.grayscale(sharpened_image) if grayscale else sharpened_image

        # Flip
        flip_option = st.sidebar.selectbox("Flip Image", ["None", "Horizontal", "Vertical"])
        if flip_option == "Horizontal":
            edited_image = ImageOps.mirror(edited_image)
        elif flip_option == "Vertical":
            edited_image = ImageOps.flip(edited_image)

        # Crop
        crop = st.sidebar.checkbox("Crop Image")
        if crop:
            left = st.sidebar.number_input("Left", 0, edited_image.width, 0)
            top = st.sidebar.number_input("Top", 0, edited_image.height, 0)
            right = st.sidebar.number_input("Right", 0, edited_image.width, edited_image.width)
            bottom = st.sidebar.number_input("Bottom", 0, edited_image.height, edited_image.height)
            edited_image = edited_image.crop((left, top, right, bottom))

        st.image(edited_image, caption="Edited Image", use_column_width=True)

        # Download Button
        buffered = io.BytesIO()
        edited_image.save(buffered, format="JPEG")
        img_str = buffered.getvalue()
        st.download_button(
            "Download Edited Image",
            img_str,
            file_name="edited_image.jpg",
            mime="image/jpeg",
        )

if __name__ == "__main__":
    main()
