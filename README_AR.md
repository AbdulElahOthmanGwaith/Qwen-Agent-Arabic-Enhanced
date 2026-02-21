# Qwen-Agent مع دعم اللغة العربية المحسّن

<p align="center">
    <img src="https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/logo_qwen_agent.png" width="400"/>
<p>

## نظرة عامة

**Qwen-Agent** هو إطار عمل قوي لتطوير تطبيقات الذكاء الاصطناعي بناءً على نموذج Qwen. يوفر إمكانيات متقدمة مثل:
- اتباع التعليمات بدقة
- استخدام الأدوات والوظائف
- التخطيط والتفكير المتقدم
- إدارة الذاكرة والسياق

هذا الإصدار المحسّن يضيف **دعماً شاملاً للغة العربية** مع أدوات متخصصة لمعالجة النصوص العربية.

## الميزات الجديدة

### 🎤 أداة تحويل النص إلى كلام (TTS)
تحويل النصوص العربية والإنجليزية إلى ملفات صوتية بجودة عالية.

```python
bot = Assistant(
    llm=llm_cfg,
    function_list=['text_to_speech'],
    system_message='أنت مساعد ذكي'
)
```

### 🔤 أداة معالجة النصوص العربية
معالجة متقدمة للنصوص العربية تشمل:
- إزالة التشكيل
- تطبيع النصوص
- استخراج الكلمات المفتاحية

```python
bot = Assistant(
    llm=llm_cfg,
    function_list=['arabic_text_processor'],
    system_message='أنت مساعد ذكي'
)
```

### 🌍 دعم كامل للغة العربية
- قوالب معرفة بالعربية
- تنسيق التواريخ بالعربية
- رسائل نظام بالعربية

## البدء السريع

### التثبيت

```bash
# من PyPI
pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"

# من المصدر
git clone https://github.com/AbdulElahOthmanGwaith/Qwen-Agent-Arabic-Enhanced.git
cd Qwen-Agent-Arabic-Enhanced
pip install -e ".[gui,rag,code_interpreter,mcp]"
```

### مثال بسيط

```python
from qwen_agent.agents import Assistant

# إعداد نموذج اللغة
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
}

# إنشاء وكيل ذكي
bot = Assistant(
    llm=llm_cfg,
    system_message='أنت مساعد ذكي يتحدث العربية',
    function_list=['text_to_speech', 'arabic_text_processor', 'code_interpreter']
)

# استخدام الوكيل
messages = [{'role': 'user', 'content': 'مرحبا، كيف يمكنك مساعدتي؟'}]
for response in bot.run(messages=messages, lang='ar'):
    print(response)
```

### تشغيل واجهة ويب

```python
from qwen_agent.gui import WebUI

bot = Assistant(
    llm=llm_cfg,
    system_message='أنت مساعد ذكي',
    function_list=['text_to_speech', 'arabic_text_processor']
)

# إعدادات الواجهة
config = {
    'user.name': 'أنت',
    'input.placeholder': 'اسأل أي سؤال بالعربية...',
    'prompt.suggestions': [
        'ما هو الذكاء الاصطناعي؟',
        'اشرح لي البرمجة',
        'كيف أتعلم اللغة الإنجليزية؟'
    ]
}

# تشغيل الواجهة
ui = WebUI(bot, chatbot_config=config)
ui.run(server_port=7860)
```

## الأدوات المتاحة

### الأدوات المدمجة الأصلية
- `code_interpreter`: تنفيذ الكود بأمان
- `web_search`: البحث على الويب
- `image_gen`: توليد الصور
- `doc_parser`: تحليل المستندات
- وغيرها...

### الأدوات الجديدة
- `text_to_speech`: تحويل النص إلى كلام
- `arabic_text_processor`: معالجة النصوص العربية

## التوثيق الشامل

للمزيد من المعلومات والأمثلة المتقدمة، انظر:
- [ARABIC_ENHANCEMENTS.md](./ARABIC_ENHANCEMENTS.md) - توثيق التحسينات العربية
- [examples/](./examples/) - أمثلة عملية
- [الموقع الرسمي](https://qwenlm.github.io/Qwen-Agent/en/)

## الأمثلة

### مثال 1: وكيل يقرأ الملفات ويستخدم الأدوات

```python
from qwen_agent.agents import Assistant

system_instruction = '''أنت مساعد ذكي متخصص في:
- قراءة وتحليل الملفات
- الإجابة على الأسئلة
- تحويل النصوص إلى كلام'''

bot = Assistant(
    llm=llm_cfg,
    system_message=system_instruction,
    function_list=['text_to_speech', 'code_interpreter'],
    files=['document.pdf']
)

messages = [{'role': 'user', 'content': 'اقرأ الملف وأخبرني عن محتواه'}]
for response in bot.run(messages=messages, lang='ar'):
    print(response)
```

### مثال 2: معالجة النصوص العربية

```python
messages = [{
    'role': 'user',
    'content': 'أزل التشكيل من هذا النص: مَرْحَبًا بِكَ فِي عَالَمِ الذَّكَاءِ الاصْطِنَاعِيِّ'
}]

for response in bot.run(messages=messages, lang='ar'):
    print(response)
```

## المتطلبات

- Python 3.8 أو أحدث
- متصفح حديث (لواجهة الويب)
- مفتاح API من DashScope (اختياري)

## الإعدادات

### متغيرات البيئة

```bash
# مفتاح API من DashScope
export DASHSCOPE_API_KEY="your_api_key"

# إعدادات الوكيل
export QWEN_AGENT_DEFAULT_WORKSPACE="workspace"
export QWEN_AGENT_MAX_LLM_CALL_PER_RUN="20"
```

## الترخيص

هذا المشروع مرخص تحت رخصة Apache License 2.0.

## المساهمة

نرحب بمساهماتكم! يرجى:
1. فتح issue لمناقشة الميزة
2. عمل fork للمستودع
3. إنشاء pull request

## الدعم

- 📧 البريد الإلكتروني: support@example.com
- 💬 Discord: [انضم إلى المجتمع](https://discord.gg/CV4E9rpNSD)
- 📖 التوثيق: [qwenlm.github.io](https://qwenlm.github.io/Qwen-Agent/en/)

## الروابط المهمة

- [المستودع الأصلي](https://github.com/QwenLM/Qwen-Agent)
- [نموذج Qwen](https://huggingface.co/Qwen)
- [DashScope API](https://help.aliyun.com/zh/dashscope/)

---

**تم التطوير بواسطة:** Manus AI  
**آخر تحديث:** فبراير 2026  
**الإصدار:** 1.0.0
