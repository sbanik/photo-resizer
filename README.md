# Image Resizer with Quality Control and Watchdog Monitoring

This is a modular **Streamlit** app that allows you to resize images with control over output width and JPEG quality. It preserves image metadata and provides an estimated file size after resizing.

---

## Features

- Upload JPEG or PNG images.
- Resize images by adjusting width with synchronized slider and number input; height auto-adjusts.
- Adjust JPEG compression quality with a slider (10 to 95).
- Preserve EXIF metadata for JPEG images.
- Show estimated output file size (in KB or MB).
- Download the resized image quickly with an updated filename suffix.
- Clean UI separation using Streamlit sidebar and main content area.
- Robust state management with graceful clearing on new uploads.
---
## Run Instructions
- Make the script executable by running: `chmod +x run.sh`
- Then you can run the script with: ```./run.sh```

---

## Dependencies

- [Streamlit](https://streamlit.io/) - For building the web app UI.
- [Pillow](https://python-pillow.org/) - Image processing.

---

## Contact

For questions or improvements, feel free to open an issue or reach out.