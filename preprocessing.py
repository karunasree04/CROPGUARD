import os
import numpy as np
import pandas as pd
import cv2
from sklearn.preprocessing import StandardScaler
try:
    from config_loader import load_config
    cfg = load_config()
except:
    cfg = {
        "image": {"normalize": True},
        "sensors": {"columns": ["soil_moisture", "air_temp", "humidity", "leaf_wetness"]}
    }

def load_hyperspectral_image(file_path):
    """Load a hyperspectral image using synthetic data for demo."""
    try:
        # For demo purposes, create synthetic hyperspectral data
        img_data = np.random.rand(100, 100, 100) * 0.8 + 0.1  # 100x100x100 bands
        print(f"Loaded synthetic hyperspectral image with shape: {img_data.shape}")
        return img_data
    except Exception as e:
        print(f"Error loading image {file_path}: {e}")
        return None

def preprocess_image(img_data, normalize=None):
    """Preprocess hyperspectral image: Handle NaNs and optional normalization."""
    if normalize is None:
        normalize = cfg["image"]["normalize"]

    img_data = np.nan_to_num(img_data)

    if normalize:
        # Scale each spectral band individually
        for i in range(img_data.shape[2]):
            band = img_data[:, :, i]
            img_data[:, :, i] = (band - np.min(band)) / (np.max(band) - np.min(band) + 1e-6)
    return img_data

def load_sensor_data(csv_path):
    """Load environmental sensor data from CSV."""
    try:
        # Create synthetic sensor data for demo
        dates = pd.date_range('2025-01-01', periods=30, freq='D')
        sensor_data = {
            'timestamp': dates,
            'soil_moisture': np.random.uniform(20, 80, 30),
            'air_temp': np.random.uniform(15, 35, 30),
            'humidity': np.random.uniform(40, 90, 30),
            'leaf_wetness': np.random.uniform(0, 10, 30)
        }
        df = pd.DataFrame(sensor_data)
        print(f"Generated synthetic sensor data with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading sensor data {csv_path}: {e}")
        return None

def preprocess_sensor_data(df):
    """Preprocess sensor data: Fill missing values and standardize numeric columns."""
    if df is None:
        return None
    df = df.copy()
    df.fillna(method='ffill', inplace=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df

def align_data(image_data, sensor_df, timestamps):
    """Align image data and sensor data based on timestamps."""
    aligned = []
    for ts in timestamps:
        # Find closest sensor reading
        closest_idx = (sensor_df['timestamp'] - ts).abs().idxmin()
        sensor_features = sensor_df.iloc[closest_idx].drop('timestamp').values
        aligned.append((image_data, sensor_features))
    return aligned

if __name__ == "__main__":
    # Example usage
    img_path = "data/samples/sample_hypercube.hdr"
    sensor_path = "data/samples/sensor_data.csv"

    img = load_hyperspectral_image(img_path)
    if img is not None:
        img_preprocessed = preprocess_image(img)
        print(f"Preprocessed image shape: {img_preprocessed.shape}")

    sensor_df = load_sensor_data(sensor_path)
    if sensor_df is not None:
        sensor_preprocessed = preprocess_sensor_data(sensor_df)
        print(f"Preprocessed sensor data shape: {sensor_preprocessed.shape}")

        # Save sample data
        sensor_df.to_csv('data/samples/sensor_data.csv', index=False)
        print("Saved sample sensor data to data/samples/sensor_data.csv")

    print("Preprocessing completed successfully!")
