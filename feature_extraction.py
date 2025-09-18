import numpy as np
try:
    from config_loader import load_config
    cfg = load_config()
except:
    cfg = {
        "image": {
            "red_band_index": 30,
            "green_band_index": 20, 
            "blue_band_index": 10,
            "nir_band_index": 60
        }
    }

def compute_ndvi(image_data):
    """Compute Normalized Difference Vegetation Index (NDVI)."""
    red_idx = cfg["image"]["red_band_index"]
    nir_idx = cfg["image"]["nir_band_index"]
    red = image_data[:, :, red_idx].astype(float)
    nir = image_data[:, :, nir_idx].astype(float)
    ndvi = (nir - red) / (nir + red + 1e-6)
    return ndvi

def compute_gndvi(image_data):
    """Compute Green Normalized Difference Vegetation Index (GNDVI)."""
    green_idx = cfg["image"]["green_band_index"]
    nir_idx = cfg["image"]["nir_band_index"]
    green = image_data[:, :, green_idx].astype(float)
    nir = image_data[:, :, nir_idx].astype(float)
    gndvi = (nir - green) / (nir + green + 1e-6)
    return gndvi

def compute_savi(image_data, L=0.5):
    """Compute Soil-Adjusted Vegetation Index (SAVI)."""
    red_idx = cfg["image"]["red_band_index"]
    nir_idx = cfg["image"]["nir_band_index"]
    red = image_data[:, :, red_idx].astype(float)
    nir = image_data[:, :, nir_idx].astype(float)
    savi = ((nir - red) / (nir + red + L + 1e-6)) * (1 + L)
    return savi

def compute_soil_index(image_data):
    """Compute Simple Soil Index."""
    red_idx = cfg["image"]["red_band_index"]
    blue_idx = cfg["image"]["blue_band_index"]
    red = image_data[:, :, red_idx].astype(float)
    blue = image_data[:, :, blue_idx].astype(float)
    si = red / (blue + 1e-6)
    return si

def extract_features(image_data):
    """Extract a dictionary of vegetation and soil indices."""
    features = {}
    features['NDVI'] = compute_ndvi(image_data)
    features['GNDVI'] = compute_gndvi(image_data)
    features['SAVI'] = compute_savi(image_data)
    features['SoilIndex'] = compute_soil_index(image_data)
    return features

if __name__ == "__main__":
    from preprocessing import load_hyperspectral_image, preprocess_image

    img_path = "data/samples/sample_hypercube.hdr"
    img = load_hyperspectral_image(img_path)
    if img is not None:
        img_preprocessed = preprocess_image(img)
        features = extract_features(img_preprocessed)
        for k, v in features.items():
            print(f"{k} shape: {v.shape}, min: {v.min():.3f}, max: {v.max():.3f}")
