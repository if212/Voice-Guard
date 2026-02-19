# VoiceGuard: Voice Cloning Attack & Detection

## One-Liner
A Gradio app with two tabs: **Attack** (clone a voice with OpenVoice v2) and **Shield** (detect fake audio with W2V-AASIST).

---

## Why This Matters
- Voice cloning now needs only **3–30 seconds** of reference audio
- Scammers clone family/executive voices for fraud (projected **$40B losses by 2027**)
- No open-source tool lets you **clone + detect** in one place

---

## Architecture

```
┌──────────────────────────────────────────────┐
│  VoiceGuard (Gradio App)                     │
│                                              │
│  [🗡️ Attack Tab]          [🛡️ Shield Tab]     │
│                                              │
│  1. Upload reference      1. Upload audio    │
│     voice (3-30 sec)         (or from Attack)│
│  2. Type text to speak    2. Click "Analyze" │
│  3. Select voice style    3. See:            │
│  4. Click "Clone"            - Verdict       │
│  5. See:                     - Confidence    │
│     - Cloned audio           - Spectrogram   │
│     - Spectrogram            - Explanation    │
│     - Similarity score                       │
│     - [Send to Shield →]                     │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Attack Tab — Voice Cloning

**Model**: OpenVoice v2 (MyShell, MIT license, 30k+ ⭐)

**Flow**:
1. Upload reference audio (3-30 sec of target voice)
2. Type any text to be spoken
3. Click "Clone & Speak"
4. Output: cloned audio, waveform, spectrogram, similarity score
5. Button: "Send to Shield →" passes audio to detection tab

**Why OpenVoice v2**: Zero-shot cloning, high quality, easy to set up, well-documented, actively maintained.

---

## Shield Tab — Deepfake Detection

**Model**: W2V-AASIST (wav2vec 2.0 + AASIST graph attention network)

**Flow**:
1. Upload audio (or receive from Attack tab)
2. Click "Analyze"
3. Output:
   - Verdict: ✅ REAL / 🚨 FAKE
   - Confidence score (0–100%)
   - Spectrogram with artifact highlighting
   - Brief explanation of why (e.g., "Unnatural spectral patterns detected at 4-8kHz")

**Why W2V-AASIST**: State-of-the-art on ASVspoof benchmarks, pretrained weights available, single model covers most attack types.

---

## Datasets

| Dataset | Use |
|---------|-----|
| ASVspoof 2019 LA | Evaluate detector (standard benchmark) |
| ASVspoof 5 (2024) | Evaluate on latest attacks |
| Self-generated (via Attack tab) | Test our cloner vs. our detector |
| LibriSpeech (subset) | Real speech samples for testing |

---

## Timeline

### Phase 1: Setup & Proposal (Feb 17–20)
| Task | Owner |
|------|-------|
| Set up repo, conda env, Gradio skeleton | Person A |
| Test OpenVoice v2 cloning on sample audio | Person A |
| Test W2V-AASIST inference on ASVspoof samples | Person B |
| **Submit proposal slides (Feb 20)** | Both |

### Phase 2: Build (Feb 24–Mar 13)
| Task | Owner |
|------|-------|
| Attack tab: OpenVoice pipeline + UI (upload, clone, playback, spectrogram) | Person A |
| Shield tab: W2V-AASIST pipeline + UI (upload, analyze, verdict, spectrogram) | Person B |
| Connect tabs: "Send to Shield" button | Both |
| **Progress meeting slides (Mar 13)** | Both |

### Phase 3: Evaluate & Improve (Mar 17–Apr 10)
| Task | Owner |
|------|-------|
| Evaluate detector on ASVspoof 2019/5 (EER, accuracy) | Person B |
| Test detector against our own cloned audio | Person A |
| Test robustness: add phone noise/compression to cloned audio, re-test | Person A |
| Analyze results, identify failure cases | Both |
| **Challenge analysis slides (Apr 10)** | Both |

### Phase 4: Polish & Present (Apr 14–22)
| Task | Owner |
|------|-------|
| Polish UI, add explanations, handle edge cases | Person A |
| Write README, record demo video | Person B |
| **Final slides (Apr 17), Final presentation (Apr 20/22)** | Both |

---

## Tech Stack

| What | Tool |
|------|------|
| UI | Gradio |
| Voice cloning | OpenVoice v2 |
| Deepfake detection | W2V-AASIST |
| Audio processing | librosa, torchaudio |
| Visualization | matplotlib (spectrograms) |
| Metrics | scikit-learn (EER, ROC) |
| Compute | CMU GPU cluster / Colab |

---

## Cost: $0
All models are open source. All datasets are free for academic use.

---

## Key References
1. OpenVoice v2 — github.com/myshell-ai/OpenVoice
2. W2V-AASIST — github.com/TakHemlata/SSL_Anti-spoofing
3. ASVspoof 5 (2024) — Latest spoofing detection challenge
4. ASVspoof 2019 LA — Standard benchmark dataset
