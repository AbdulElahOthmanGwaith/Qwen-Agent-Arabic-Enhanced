# إضافات جديدة - فبراير 2026

## 1. أداة تحويل الكلام إلى نص (Speech-to-Text)

**الملف:** `arabic_speech_to_text.py`

تحويل الملفات الصوتية إلى نص مكتوب باستخدام نموذج Whisper.

### المتطلبات:
```bash
pip install torch transformers
# أو للإصدار الأسرع:
pip install faster-whisper
```

### الاستخدام:
```python
from qwen_agent.agents import Assistant

llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
}

bot = Assistant(
    llm=llm_cfg,
    function_list=['arabic_speech_to_text'],
    system_message='أنت مساعد ذكي يتحدث العربية'
)

# تحويل الصوت إلى نص
messages = [{'role': 'user', 'content': 'حوّل هذا الملف إلى نص: /path/to/audio.mp3'}]
response = bot.run(messages=messages)
```

### المعلمات:
- `audio_path`: مسار ملف الصوت (مطلوب)
- `language`: لغة الصوت (默认: ar)
- `task`: نوع التحويل (transcribe أو translate)

---

## 2. أداة فحص الإملاء العربي (Spell Checker)

**الملف:** `arabic_spell_checker.py`

فحص النصوص العربية واكتشاف الأخطاء الإملائية.

### الاستخدام:
```python
from qwen_agent.agents import Assistant

bot = Assistant(
    llm=llm_cfg,
    function_list=['arabic_spell_checker'],
    system_message='أنت مساعد ذكي يتحدث العربية'
)

# فحص النص
messages = [{'role': 'user', 'content': 'افحص هذا النص: مرحبا كيف حالك'}]
response = bot.run(messages=messages)
```

### المعلمات:
- `text`: النص المراد فحصه (مطلوب)
- `check_diacritics`: فحص علامات التشكيل
- `suggest_corrections`: اقتراح تصحيحات

---

## 3. أداة تطبيع النصوص (Text Normalizer)

**الملف:** `arabic_spell_checker.py`

تطبيع النصوص العربية - إزالة التشكيل وتوحيد الحروف.

### الاستخدام:
```python
bot = Assistant(
    llm=llm_cfg,
    function_list=['arabic_text_normalizer'],
    system_message='أنت مساعد ذكي يتحدث العربية'
)

messages = [{'role': 'user', 'content': 'طبيع هذا النص: مَرْحَبًا بِكَ'}]
response = bot.run(messages=messages)
```

---

## التحديثات في ملف الأدوات

أضف الأدوات الجديدة في `qwen_agent/tools/__init__.py`:

```python
from qwen_agent.tools.arabic_speech_to_text import ArabicSpeechToText
from qwen_agent.tools.arabic_spell_checker import ArabicSpellChecker, ArabicTextNormalizer
```

---

## قائمة الأدوات المحدثة

| الأداة | الوصف |
|--------|-------|
| `arabic_speech_to_text` | تحويل الكلام إلى نص |
| `arabic_speech_to_text_fast` | تحويل الكلام إلى نص (نسخة سريعة) |
| `arabic_spell_checker` | فحص الإملاء العربي |
| `arabic_text_normalizer` | تطبيع النصوص العربية |
| `text_to_speech` | تحويل النص إلى كلام |
| `arabic_text_processor` | معالجة النصوص العربية |
| `arabic_doc_parser` | تحليل المستندات العربية |

---

## التطويرات المستقبلية المخططة

- [ ] دعم اللهجات العربية (يمنية، مصرية، خليجية)
- [ ] تحسين أداء التعرف على الكلام
- [ ] إضافة قاموس أكبر للكلمات العربية
- [ ] دعم التدقيق النحوي

---

**آخر تحديث:** فبراير 2026
