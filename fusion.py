import numpy as np
import pandas as pd

def flatten_image_features(feature_dict):
    """Flatten 2D spatial feature maps into 1D vectors for fusion."""
    flat_features = {}
    for k, v in feature_dict.items():
        flat_features[k] = v.flatten()
    return flat_features

def fuse_features(image_features, sensor_features):
    """Fuse image features with sensor features."""
    flat_image = flatten_image_features(image_features)
    image_matrix = np.stack(list(flat_image.values()), axis=1)

    # Repeat sensor features for each pixel
    sensor_matrix = np.tile(sensor_features, (image_matrix.shape[0], 1))

    # Concatenate along columns
    fused_matrix = np.concatenate([image_matrix, sensor_matrix], axis=1)
    return fused_matrix

def create_fused_dataframe(image_features, sensor_features, sensor_columns=None):
    """Return a pandas DataFrame combining image and sensor features."""
    flat_image = flatten_image_features(image_features)
    image_df = pd.DataFrame(flat_image)

    if sensor_columns is None:
        sensor_columns = [f'sensor_{i}' for i in range(len(sensor_features))]
    sensor_df = pd.DataFrame([sensor_features]*image_df.shape[0], columns=sensor_columns)

    fused_df = pd.concat([image_df, sensor_df], axis=1)
    return fused_df

if __name__ == "__main__":
    from preprocessing import load_hyperspectral_image, preprocess_image, load_sensor_data, preprocess_sensor_data
    from feature_extraction import extract_features

    # Load data
    img_path = "data/samples/sample_hypercube.hdr"
    sensor_path = "data/samples/sensor_data.csv"

    img = load_hyperspectral_image(img_path)
    img_preprocessed = preprocess_image(img)
    sensor_df = preprocess_sensor_data(load_sensor_data(sensor_path))

    # Extract features
    image_features = extract_features(img_preprocessed)
    sensor_features = sensor_df.iloc[0].drop('timestamp').values

    # Fuse features
    fused_array = fuse_features(image_features, sensor_features)
    fused_df = create_fused_dataframe(image_features, sensor_features, 
                                    sensor_columns=list(sensor_df.columns[1:]))

    print("Fused feature array shape:", fused_array.shape)
    print("Fused dataframe shape:", fused_df.shape)
    print(fused_df.head())
