# -*- coding: utf-8 -*-
"""
أداة تحويل الكلام إلى نص (Speech-to-Text)
Arabic Speech-to-Text Tool
"""

import json
import os
import base64
from typing import Union

try:
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModelForSpeechSeq2Seq
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('arabic_speech_to_text')
class ArabicSpeechToText(BaseTool):
    """
    أداة متخصصة لتحويل الكلام العربي إلى نص مكتوب.
    Supports Arabic and other languages with Whisper model.
    """
    
    description = 'أداة تحويل الكلام إلى نص - تتلقى ملف صوتي وتُرجع النص المكتوب'
    parameters = [
        {
            'name': 'audio_path',
            'type': 'string',
            'description': 'مسار ملف الصوت (MP3, WAV, M4A, etc.)',
            'required': True
        },
        {
            'name': 'language',
            'type': 'string',
            'description': 'لغة الملف الصوتي (默认: Arabic). Options: ar, en, auto',
            'required': False,
            'default': 'ar'
        },
        {
            'name': 'task',
            'type': 'string',
            'description': 'نوع التحويل: transcribe أو translate',
            'required': False,
            'default': 'transcribe'
        }
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.tokenizer = None
        self.device = None
        self.pipeline_init = False
    
    def _init_pipeline(self):
        """Initialize Whisper model pipeline"""
        if self.pipeline_init:
            return
            
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "يرجى تثبيت المكتبات المطلوبة: pip install torch transformers"
            )
        
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        model_id = "openai/whisper-base"
        
        print(f"جاري تحميل نموذج Whisper على: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=self.dtype
        ).to(self.device)
        
        self.pipeline = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.tokenizer,
            feature_extractor=self.tokenizer,
            max_new_tokens=256,
            torch_dtype=self.dtype,
            device=self.device,
        )
        
        self.pipeline_init = True
    
    def call(self, params: str, **kwargs) -> str:
        """تحويل الصوت إلى نص"""
        import json5
        params = json5.loads(params)
        
        audio_path = params.get('audio_path')
        language = params.get('language', 'ar')
        task = params.get('task', 'transcribe')
        
        if not audio_path:
            return json.dumps({
                'success': False,
                'error': 'يرجى توفير مسار ملف الصوت'
            }, ensure_ascii=False)
        
        if not os.path.exists(audio_path):
            return json.dumps({
                'success': False,
                'error': f'الملف غير موجود: {audio_path}'
            }, ensure_ascii=False)
        
        try:
            # Initialize if needed
            if not self.pipeline_init:
                self._init_pipeline()
            
            # Prepare kwargs
            generate_kwargs = {
                "task": task,
                "max_new_tokens": 256,
            }
            
            if language != 'auto':
                generate_kwargs["language"] = language
            
            # Run transcription
            result = self.pipeline(audio_path, **generate_kwargs)
            
            return json.dumps({
                'success': True,
                'text': result['text'],
                'language': language,
                'audio_file': audio_path
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
    
    def _cleanup(self):
        """Clean up resources"""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        self.pipeline_init = False
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# Alternative: Fallback using faster-whisper if available
try:
    from faster_whisper import WhisperModel
    
    @register_tool('arabic_speech_to_text_fast')
    class ArabicSpeechToTextFast(BaseTool):
        """
        إصدار أسرع من أداة تحويل الكلام إلى نص باستخدام faster-whisper
        """
        
        description = 'أداة تحويل الكلام إلى نص (نسخة سريعة)'
        parameters = [
            {
                'name': 'audio_path',
                'type': 'string',
                'description': 'مسار ملف الصوت',
                'required': True
            },
            {
                'name': 'model_size',
                'type': 'string',
                'description': 'حجم النموذج: tiny, base, small, medium, large',
                'required': False,
                'default': 'base'
            },
            {
                'name': 'language',
                'type': 'string',
                'description': 'لغة الملف الصوتي',
                'required': False,
                'default': 'ar'
            }
        ]
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.model = None
            self.model_size = 'base'
        
        def _get_model(self, model_size: str):
            if self.model is None or self.model_size != model_size:
                self.model = WhisperModel(
                    model_size,
                    device="cuda" if torch.cuda.is_available() else "cpu",
                    compute_type="float16" if torch.cuda.is_available() else "int8"
                )
                self.model_size = model_size
        
        def call(self, params: str, **kwargs) -> str:
            import json5
            params = json5.loads(params)
            
            audio_path = params.get('audio_path')
            model_size = params.get('model_size', 'base')
            language = params.get('language', 'ar')
            
            if not audio_path or not os.path.exists(audio_path):
                return json.dumps({
                    'success': False,
                    'error': 'الملف غير موجود'
                }, ensure_ascii=False)
            
            try:
                self._get_model(model_size)
                
                segments, info = self.model.transcribe(
                    audio_path,
                    language=language,
                    beam_size=5,
                    vad_filter=True
                )
                
                text = " ".join([segment.text for segment in segments])
                
                return json.dumps({
                    'success': True,
                    'text': text,
                    'language': info.language,
                    'probability': info.language_probability,
                    'audio_file': audio_path
                }, ensure_ascii=False)
                
            except Exception as e:
                return json.dumps({
                    'success': False,
                    'error': str(e)
                }, ensure_ascii=False)

except ImportError:
    pass  # faster-whisper not available, use transformers version
