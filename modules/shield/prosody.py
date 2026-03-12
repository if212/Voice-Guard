import librosa
import numpy as np


def _compute_jitter(f0_voiced):
    """Pitch period micro-perturbation: mean(|T_i - T_{i+1}|) / T_mean.

    Jitter measures cycle-to-cycle pitch variation.
    Real speech has natural jitter; AI speech tends to be more stable.
    """
    if len(f0_voiced) < 5:
        return 0.0

    # Convert F0 (Hz) to period T (seconds)
    periods = 1.0 / f0_voiced
    diffs = np.abs(np.diff(periods))
    mean_period = np.mean(periods)

    if mean_period == 0:
        return 0.0
    return float(np.mean(diffs) / mean_period)


def _compute_shimmer(y, sr, f0, voiced_flag):
    """Amplitude cycle-to-cycle variation: mean(|A_i - A_{i+1}|) / A_mean.

    Shimmer measures amplitude perturbation per pitch period.
    Real speech has natural shimmer; AI speech tends to be smoother.
    """
    hop = 512
    amplitudes = []

    for i in range(len(f0)):
        if not voiced_flag[i] or np.isnan(f0[i]) or f0[i] == 0:
            continue
        center = i * hop
        period = int(sr / f0[i])
        start = max(0, center - period // 2)
        end = min(len(y), center + period // 2)
        if end > start:
            amplitudes.append(float(np.max(np.abs(y[start:end]))))

    if len(amplitudes) < 5:
        return 0.0

    amps = np.array(amplitudes)
    diffs = np.abs(np.diff(amps))
    mean_amp = np.mean(amps)

    if mean_amp == 0:
        return 0.0
    return float(np.mean(diffs) / mean_amp)


def analyze_prosody(audio_path: str) -> dict:
    """Extract voice quality and prosody features for explainability (no scoring).

    Returns raw feature values + plot data for UI rendering.
    """
    y, sr = librosa.load(audio_path, sr=None)

    # Truncate to first 10s (pyin is slow on long files)
    y = y[: sr * 10]

    # F0 extraction
    f0, voiced_flag, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),   # ~65 Hz
        fmax=librosa.note_to_hz("C7"),   # ~2093 Hz
        sr=sr,
    )
    f0_voiced = f0[voiced_flag] if np.any(voiced_flag) else np.array([])

    # F0 statistics
    f0_mean = float(np.mean(f0_voiced)) if len(f0_voiced) >= 5 else 0.0
    f0_std = float(np.std(f0_voiced)) if len(f0_voiced) >= 5 else 0.0
    f0_cv = (f0_std / f0_mean) if f0_mean > 0 else 0.0

    # Jitter & Shimmer
    jitter = _compute_jitter(f0_voiced)
    shimmer = _compute_shimmer(y, sr, f0, voiced_flag)

    # Energy
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    energy_cv = float(np.std(rms) / np.mean(rms)) if len(rms) >= 5 and np.mean(rms) > 0 else 0.0

    return {
        "jitter": round(jitter, 6),
        "shimmer": round(shimmer, 6),
        "f0_mean": round(f0_mean, 1),
        "f0_std": round(f0_std, 1),
        "f0_cv": round(f0_cv, 4),
        "energy_cv": round(energy_cv, 4),
        "plot_data": {
            "f0": f0,
            "voiced_flag": voiced_flag,
            "rms": rms,
            "sr": sr,
            "hop_length": 512,
        },
    }
