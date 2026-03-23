import argparse
import os
import sys

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    from pillow_heif import register_heif_opener
    
    # Force Pillow to understand Apple's HEIC format
    register_heif_opener()
except ImportError:
    print("[-] Error: Required libraries are missing.")
    print("[*] Please install them using: pip install Pillow pillow-heif")
    sys.exit(1)

def get_exif_data(image_path):
    """Extracts basic EXIF metadata from JPG, TIFF, and HEIC images."""
    try:
        image = Image.open(image_path)
        
        # Modern way to get EXIF in Pillow (works better with HEIC)
        exif = image.getexif()
        
        if not exif:
            print("[-] No EXIF metadata found in this image.")
            return None, None

        exif_data = {}
        gps_data = {}

        # Extract standard EXIF tags
        for tag_id, value in exif.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_data[tag_name] = value

        # Extract GPS Info (0x8825 is the hex code for GPSInfo IFD)
        gps_ifd = exif.get_ifd(0x8825)
        if gps_ifd:
            for tag_id, value in gps_ifd.items():
                gps_tag_name = GPSTAGS.get(tag_id, tag_id)
                gps_data[gps_tag_name] = value

        return exif_data, gps_data

    except Exception as e:
        print(f"[-] Error processing image: {e}")
        return None, None

def convert_to_degrees(value):
    """Converts GPS coordinates (Degrees, Minutes, Seconds) to Decimal Degrees."""
    try:
        # Pillow sometimes returns IFDRational objects, we need to convert them to float
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except (IndexError, TypeError, ValueError) as e:
        return None

def extract_gps_coordinates(gps_data):
    """Extracts and converts latitude and longitude to decimal format."""
    if not gps_data:
        return None

    try:
        lat_data = gps_data.get("GPSLatitude")
        lat_ref = gps_data.get("GPSLatitudeRef")
        lon_data = gps_data.get("GPSLongitude")
        lon_ref = gps_data.get("GPSLongitudeRef")

        if lat_data and lat_ref and lon_data and lon_ref:
            lat = convert_to_degrees(lat_data)
            lon = convert_to_degrees(lon_data)

            if lat is None or lon is None:
                return None

            # If the reference is South or West, the coordinate is negative
            if lat_ref == "S":
                lat = -lat
            if lon_ref == "W":
                lon = -lon

            return lat, lon
    except Exception:
        pass
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Advanced OSINT Image Metadata & GPS Extractor")
    parser.add_argument("-i", "--image", required=True, help="Path to the image file (e.g., photo.jpg or photo.heic)")
    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print(f"[-] Error: File '{args.image}' not found.")
        sys.exit(1)

    print("="*65)
    print("📸 Advanced OSINT Image Metadata Extractor (HEIC Supported)")
    print("="*65)
    print(f"[*] Analyzing : {args.image}\n")

    exif_data, gps_data = get_exif_data(args.image)

    if exif_data:
        print("[+] Basic Metadata Found:")
        interesting_keys = ['Make', 'Model', 'Software', 'DateTimeOriginal', 'OSVersion']
        found_any = False
        for key in interesting_keys:
            if key in exif_data:
                print(f" ╰──> {key:<20}: {exif_data[key]}")
                found_any = True
        if not found_any:
            print(" ╰──> Only structural data found (no camera info).")

    if gps_data:
        coordinates = extract_gps_coordinates(gps_data)
        if coordinates:
            lat, lon = coordinates
            print("\n[+] GPS Coordinates Found!")
            print(f" ╰──> Latitude  : {lat:.6f}")
            print(f" ╰──> Longitude : {lon:.6f}")
            
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            print(f" ╰──> Google Maps : {maps_url}")
        else:
            print("\n[-] GPS data structure found but could not be parsed.")
    else:
        print("\n[-] No GPS tracking data found in this image.")
        print("[!] Note: Social media, email clients, and device privacy settings often strip this data.")

    print("="*65)

if __name__ == "__main__":
	main()
