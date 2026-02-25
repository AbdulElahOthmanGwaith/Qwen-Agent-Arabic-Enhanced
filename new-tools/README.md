# Qwen-Agent Arabic Enhanced - February 2026 Updates

## New Tools Added

### 1. Arabic Speech-to-Text (STT)
Convert Arabic speech to text using Whisper model.

**File:** `arabic_speech_to_text.py`

### 2. Arabic Spell Checker
Check Arabic text for spelling errors.

**File:** `arabic_spell_checker.py`

### 3. Arabic Text Normalizer
Normalize Arabic text - remove diacritics and unify letters.

**File:** `arabic_spell_checker.py` (included)

---

## Installation

```bash
pip install torch transformers
# or for faster version:
pip install faster-whisper
```

## Usage

```python
from qwen_agent.agents import Assistant

llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
}

bot = Assistant(
    llm=llm_cfg,
    function_list=['arabic_speech_to_text', 'arabic_spell_checker'],
    system_message='أنت مساعد ذكي يتحدث العربية'
)
```

---

**Last Updated:** February 2026
