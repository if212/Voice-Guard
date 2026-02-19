import os
import sys
import argparse

# Ensure the OpenVoice package is importable
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OPENVOICE_ROOT = os.path.join(PROJECT_ROOT, "OpenVoice")
sys.path.insert(0, OPENVOICE_ROOT)

import gradio as gr

from modules.attack.clone import VoiceCloner
from modules.attack.ui import build_attack_tab


def main():
    parser = argparse.ArgumentParser(description="VoiceGuard")
    parser.add_argument("--share", action="store_true", help="Create a public Gradio link")
    parser.add_argument("--device", type=str, default=None, help="Force device (cpu, cuda:0)")
    args = parser.parse_args()

    cloner = VoiceCloner(openvoice_root=OPENVOICE_ROOT, device=args.device)

    with gr.Blocks(title="VoiceGuard") as app:
        gr.Markdown("# VoiceGuard: Voice Cloning Attack & Detection")

        with gr.Tab("Attack"):
            build_attack_tab(cloner)

        with gr.Tab("Shield"):
            gr.Markdown("*Shield tab coming soon — deepfake audio detection.*")

    app.queue()
    app.launch(share=args.share)


if __name__ == "__main__":
    main()
