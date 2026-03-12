import librosa
import numpy as np


def analyze_spectral(audio_path: str) -> dict:
    """Extract spectral features for explainability (no scoring).

    Returns raw feature values for display in the UI.
    """
    y, sr = librosa.load(audio_path, sr=None)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=2048, hop_length=512)
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=2048, hop_length=512)
    flatness = librosa.feature.spectral_flatness(y=y, n_fft=2048, hop_length=512)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85, n_fft=2048, hop_length=512)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=2048, hop_length=512)

    return {
        "spectral_centroid": round(float(np.mean(centroid)), 1),
        "spectral_bandwidth": round(float(np.mean(bandwidth)), 1),
        "spectral_flatness": round(float(np.mean(flatness)), 6),
        "spectral_rolloff": round(float(np.mean(rolloff)), 1),
        "spectral_contrast": [round(float(c), 2) for c in np.mean(contrast, axis=1)],
        "sample_rate": int(sr),
    }
