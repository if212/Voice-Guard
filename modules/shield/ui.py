import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import gradio as gr

from modules.shield.detect import DeepfakeDetector


def _plot_spectrogram(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    fig, ax = plt.subplots(figsize=(8, 3))
    librosa.display.specshow(S_dB, sr=sr, x_axis="time", y_axis="mel", ax=ax)
    ax.set_title("Mel Spectrogram")
    fig.colorbar(ax.collections[0], ax=ax, format="%+2.0f dB")
    fig.tight_layout()
    return fig


def build_shield_tab(detector: DeepfakeDetector):
    """Build the Shield tab UI. Must be called inside a gr.Tab context.

    Returns:
        audio_input component (for "Send to Shield" wiring from Attack tab).
    """

    gr.Markdown(
        "Upload an audio file (or receive from Attack tab) to analyze "
        "whether it is real or AI-generated."
    )

    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                label="Audio to Analyze",
                type="filepath",
            )
            analyze_button = gr.Button("Analyze", variant="primary")

        with gr.Column(scale=1):
            verdict_md = gr.Markdown(value="*Upload audio and click Analyze*")
            confidence_num = gr.Number(label="Confidence (%)", interactive=False)
            spoof_score = gr.Number(label="W2V-AASIST Spoof Probability", interactive=False)

    spectrogram_plot = gr.Plot(label="Spectrogram")

    def on_analyze(audio_path):
        try:
            if not audio_path:
                return "*Please upload an audio file first.*", None, None, None

            result = detector.detect(audio_path)

            verdict = result["verdict"]
            if verdict == "FAKE":
                verdict_html = f"### 🚨 Verdict: **FAKE** — Confidence: {result['confidence']}%"
            elif verdict == "SUSPICIOUS":
                verdict_html = f"### ⚠️ Verdict: **SUSPICIOUS** — Confidence: {result['confidence']}%"
            else:
                verdict_html = f"### ✅ Verdict: **REAL** — Confidence: {result['confidence']}%"

            spec_fig = _plot_spectrogram(audio_path)

            return verdict_html, result["confidence"], result["spoof_prob"], spec_fig
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"### Error: {e}", None, None, None

    analyze_button.click(
        fn=on_analyze,
        inputs=[audio_input],
        outputs=[verdict_md, confidence_num, spoof_score, spectrogram_plot],
    )

    return audio_input
