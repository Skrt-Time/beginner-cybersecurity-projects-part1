# 09 - Advanced OSINT Image Metadata Extractor (HEIC Supported)

A Digital Forensics and OSINT (Open Source Intelligence) Python utility designed to extract hidden EXIF metadata from image files. Unlike basic extractors, this tool includes support for Apple's **HEIC (High-Efficiency Image Container)** format, making it highly relevant for modern mobile forensics. 

This tool demonstrates the privacy risks associated with sharing raw smartphone images by automatically extracting the camera model, timestamps, and converting embedded GPS coordinates into a functional Google Maps link.

## ⚠️ Educational Disclaimer
**This tool is strictly for educational purposes and privacy awareness.** It should only be used on images you own or have explicit permission to analyze. Do not use this tool for stalking or compromising the privacy of individuals without their consent.

## ✨ Key Features
* **Modern Format Support:** Bypasses standard library limitations by utilizing `pillow-heif` to read raw iOS `.HEIC` files alongside standard `.JPG` and `.TIFF` files.
* **Metadata Extraction:** Reads embedded metadata to identify the device manufacturer, model, and software version used to take the photo.
* **Geolocator:** Extracts raw GPS tracking data directly from the image's IFD (Image File Directory) tags.
* **Coordinate Conversion:** Automatically performs the mathematical conversion from DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees) using the standard formula:
  $DD = d + \frac{m}{60} + \frac{s}{3600}$
* **Mapping Integration:** Generates a direct Google Maps URL for immediate geographic visualization of where the photo was taken.

## ⚙️ Prerequisites & Installation
This script requires the third-party `Pillow` and `pillow-heif` libraries to process advanced image files.

1. **Activate your virtual environment** (Recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install the dependencies:**
```bash
pip install -r requirements.txt
```

### 🛡️ Note on Repository Maintenance (.gitignore)
When testing this tool with your own smartphone photos, ensure those personal images are not uploaded to your public GitHub repository. A `.gitignore` file is provided in this directory to automatically block all `*.heic`, `*.jpg`, and `*.png` files from being committed.

## 📖 Help Menu
You can access the built-in manual by running the `-h` or `--help` command:

```bash
python exif_tracker.py --help
```

**Output:**
```text
usage: exif_tracker.py [-h] -i IMAGE

Advanced OSINT Image Metadata & GPS Extractor

options:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Path to the image file (e.g., photo.jpg or photo.heic)
```

## 💻 Command Examples

### Analyzing a Modern Smartphone Image
Run the script against a raw photo transferred directly via USB cable (ensure location services were enabled on the camera app):
```bash
python exif_tracker.py -i evidence_01.heic
```

## 🧠 OPSEC Note: The Reality of GPS Data
If the script reports `No GPS tracking data found`, it is usually due to one of two reasons:
1. **Platform Stripping:** Most social media platforms (WhatsApp, Twitter, Instagram) and cloud transfer services automatically strip EXIF data upon upload to protect user privacy. To analyze an image, you need the *original, raw file*.
2. **Device Privacy Settings:** Modern operating systems (like iOS) allow users to disable "Precise Location" for the Camera app, meaning the phone simply never recorded the coordinates when the photo was taken.

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Directory Scanning:** Allow the script to ingest an entire folder of images and generate a `.kml` file to map a target's physical movements over time on Google Earth.
2. **Metadata Stripping:** Add a `-c` (clean) flag that automatically deletes all EXIF data from the image and saves a privacy-safe copy.
