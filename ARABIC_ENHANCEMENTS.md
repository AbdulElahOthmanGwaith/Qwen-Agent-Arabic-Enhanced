# تحسينات دعم اللغة العربية في Qwen-Agent

## نظرة عامة

تم تطوير مجموعة من التحسينات والإضافات لتعزيز دعم اللغة العربية في إطار عمل Qwen-Agent. تشمل هذه التحسينات أدوات جديدة وتحديثات لغوية شاملة.

## التطويرات المنجزة

### 1. أداة تحويل النص إلى كلام (Text-to-Speech Tool)

**الملف:** `qwen_agent/tools/text_to_speech.py`

**الوصف:**
أداة متقدمة لتحويل النصوص العربية والإنجليزية إلى ملفات صوتية MP3.

**الميزات:**
- تحويل النصوص إلى كلام بجودة عالية
- دعم اللغات المتعددة (العربية والإنجليزية وغيرها)
- إنشاء ملفات صوتية بصيغة MP3
- إدارة تلقائية لمجلد الإخراج

**الاستخدام:**
```python
from qwen_agent.agents import Assistant

bot = Assistant(
    llm=llm_cfg,
    function_list=['text_to_speech'],
    system_message='أنت مساعد ذكي'
)

# استخدام الأداة
messages = [{'role': 'user', 'content': 'حول هذا النص إلى كلام: مرحبا بك'}]
response = bot.run(messages=messages)
```

### 2. أداة معالجة النصوص العربية (Arabic Text Processor)

**الملف:** `qwen_agent/tools/arabic_text_processor.py`

**الوصف:**
أداة متخصصة لمعالجة ومعالجة النصوص العربية بطرق متقدمة.

**الميزات:**
- إزالة التشكيل (الحروف الإضافية)
- تطبيع النصوص العربية
- استخراج الكلمات المفتاحية
- إزالة كلمات التوقف الشائعة

**العمليات المدعومة:**
- `remove_diacritics`: إزالة التشكيل من النصوص
- `normalize`: تطبيع النصوص (إزالة التشكيل والتطبيع)
- `extract_keywords`: استخراج الكلمات المفتاحية من النصوص

**الاستخدام:**
```python
# إزالة التشكيل
params = {
    'text': 'مَرْحَبًا بِكَ',
    'operation': 'remove_diacritics'
}

# تطبيع النص
params = {
    'text': 'أَهْلاً وَسَهْلاً',
    'operation': 'normalize'
}

# استخراج الكلمات المفتاحية
params = {
    'text': 'الذكاء الاصطناعي هو تقنية حديثة جداً',
    'operation': 'extract_keywords'
}
```

### 3. دعم اللغة العربية في فئة Assistant

**الملف:** `qwen_agent/agents/assistant.py`

**التحسينات:**
- إضافة قوالب معرفة بالعربية
- دعم اللغة العربية في دالة `get_current_date_str()`
- تحديث نوع البيانات `Literal` لقبول 'ar' كخيار للغة

**الميزات الجديدة:**
- `KNOWLEDGE_TEMPLATE_AR`: قالب قاعدة المعرفة بالعربية
- `KNOWLEDGE_SNIPPET_AR`: قالب مقتطفات المعرفة بالعربية
- دعم كامل لتنسيق التواريخ بالعربية

**الاستخدام:**
```python
# استخدام الوكيل مع اللغة العربية
messages = [{'role': 'user', 'content': 'ما هو الذكاء الاصطناعي؟'}]
response = bot.run(messages=messages, lang='ar')
```

## ملف مثال شامل

**الملف:** `examples/assistant_arabic_enhanced.py`

يحتوي على مثال عملي شامل يوضح:
- كيفية إنشاء وكيل مع دعم اللغة العربية
- استخدام الأدوات الجديدة
- تشغيل الوكيل في وضع سطر الأوامر
- تشغيل واجهة ويب (GUI) بالعربية

## التثبيت والاستخدام

### المتطلبات الإضافية

```bash
# لأداة Text-to-Speech
pip install gtts

# للمتطلبات الأساسية
pip install qwen-agent
```

### التثبيت من المصدر

```bash
git clone https://github.com/AbdulElahOthmanGwaith/Qwen-Agent-Arabic-Enhanced.git
cd Qwen-Agent-Arabic-Enhanced
pip install -e ".[gui,rag,code_interpreter,mcp]"
```

### مثال سريع

```python
from qwen_agent.agents import Assistant

# إعداد الوكيل
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
}

bot = Assistant(
    llm=llm_cfg,
    system_message='أنت مساعد ذكي يتحدث العربية',
    function_list=['text_to_speech', 'arabic_text_processor']
)

# استخدام الوكيل
messages = [{'role': 'user', 'content': 'مرحبا، كيف حالك؟'}]
for response in bot.run(messages=messages, lang='ar'):
    print(response)
```

## الملفات المعدلة

| الملف | نوع التغيير | الوصف |
|------|-----------|-------|
| `qwen_agent/agents/assistant.py` | تحديث | إضافة دعم اللغة العربية |
| `qwen_agent/tools/__init__.py` | تحديث | تسجيل الأدوات الجديدة |

## الملفات المضافة

| الملف | الوصف |
|------|-------|
| `qwen_agent/tools/text_to_speech.py` | أداة تحويل النص إلى كلام |
| `qwen_agent/tools/arabic_text_processor.py` | أداة معالجة النصوص العربية |
| `examples/assistant_arabic_enhanced.py` | مثال شامل للاستخدام |
| `ARABIC_ENHANCEMENTS.md` | هذا الملف - التوثيق الشامل |

## الخطوات التالية والتحسينات المستقبلية

### المخطط له:
1. **دعم الكلام إلى النص (STT)**: إضافة أداة لتحويل الكلام العربي إلى نصوص
2. **تحسين معالجة النصوص**: إضافة معالجة متقدمة للنصوص العربية مثل التحليل النحوي
3. **دعم الإملاء العربي**: أداة للتحقق من الأخطاء الإملائية في النصوص العربية
4. **تحسين الأداء**: تحسين سرعة معالجة النصوص العربية الطويلة
5. **دعم اللهجات العربية**: إضافة دعم للهجات العربية المختلفة

## المساهمة

نرحب بالمساهمات والاقتراحات لتحسين دعم اللغة العربية. يرجى:
1. فتح issue لمناقشة الميزة المقترحة
2. عمل fork للمستودع
3. إنشاء pull request مع التحسينات

## الترخيص

هذا المشروع مرخص تحت رخصة Apache License 2.0. انظر ملف LICENSE للتفاصيل.

## الدعم والمساعدة

للحصول على المساعدة أو الإبلاغ عن مشاكل:
- افتح issue على GitHub
- تواصل عبر البريد الإلكتروني
- انضم إلى مجتمع Qwen على Discord

---

**آخر تحديث:** فبراير 2026
**الإصدار:** 1.0.0
