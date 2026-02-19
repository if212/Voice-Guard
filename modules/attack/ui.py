import gradio as gr

from modules.attack.clone import VoiceCloner


def build_attack_tab(cloner: VoiceCloner):
    """Build the Attack tab UI. Must be called inside a gr.Tab context."""

    gr.Markdown(
        "Upload a reference voice (3-30 seconds), type text, "
        "and generate a cloned voice speaking your text."
    )

    with gr.Row():
        with gr.Column(scale=1):
            reference_audio = gr.Audio(
                label="Reference Audio (target voice to clone)",
                type="filepath",
                value=cloner.default_reference,
            )
            text_input = gr.Textbox(
                label="Text to Speak",
                placeholder="Type the text you want the cloned voice to say...",
                lines=3,
                max_lines=6,
                value="I have an emergency! Please help me right now!",
            )
            speed_slider = gr.Slider(
                minimum=0.5, maximum=2.0, value=1.0, step=0.1,
                label="Speed",
            )
            clone_button = gr.Button("Clone & Speak", variant="primary")

        with gr.Column(scale=1):
            status_text = gr.Textbox(label="Status", interactive=False)
            output_audio = gr.Audio(label="Cloned Audio", type="filepath")

    def on_clone(text, ref_audio, speed):
        try:
            if not text or len(text.strip()) < 2:
                return "Error: Please enter at least 2 characters of text.", None
            ref = ref_audio if ref_audio else None
            output_path, sr = cloner.clone(
                text=text, reference_audio=ref, speed=speed,
            )
            return "Voice cloned successfully.", output_path
        except Exception as e:
            return f"Error: {e}", None

    clone_button.click(
        fn=on_clone,
        inputs=[text_input, reference_audio, speed_slider],
        outputs=[status_text, output_audio],
    )
