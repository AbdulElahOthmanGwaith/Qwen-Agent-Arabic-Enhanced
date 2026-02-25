# -*- coding: utf-8 -*-
"""
أداة فحص الإملاء العربي
Arabic Spell Checker Tool
"""

import json
import re
from typing import List, Dict, Union, Optional

from qwen_agent.tools.base import BaseTool, register_tool


# Dictionary of common Arabic words
COMMON_ARABIC_WORDS = {
    # Verbs
    'كان': 'كان', 'ليس': 'ليس', 'أنت': 'أنت', 'أنا': 'أنا', 'هم': 'هم',
    'نحن': 'نحن', 'أنتم': 'أنتم', 'هي': 'هي', 'هو': 'هو',
    
    # Prepositions
    'من': 'من', 'إلى': 'إلى', 'على': 'على', 'في': 'في', 'عن': 'عن',
    'منذ': 'منذ', 'بين': 'بين', 'خلال': 'خلال', 'مع': 'مع', 'بدون': 'بدون',
    
    # Conjunctions
    'و': 'و', 'ف': 'ف', 'ثم': 'ثم', 'أو': 'أو', 'لا': 'لا',
    'لم': 'لم', 'لن': 'لن', 'قد': 'قد', 'كي': 'كي', 'إن': 'إن',
    'أن': 'أن', 'كأن': 'كأن', 'لكن': 'لكن', 'لعل': 'لعل',
    
    # Common nouns
    'الله': 'الله', 'الناس': 'الناس', 'المال': 'المال', 'العلم': 'العلم',
    'الكتاب': 'الكتاب', 'القلب': 'القلب', 'العين': 'العين', 'اليد': 'اليد',
    'الرجل': 'الرجل', 'المرأة': 'المرأة', 'الولد': 'الولد', 'الفتاة': 'الفتاة',
    'البيت': 'البيت', 'الشارع': 'الشارع', 'المدينة': 'المدينة', 'القرية': 'القرية',
    'الدولة': 'الدولة', 'الحكومة': 'الحكومة', 'الشركة': 'الشركة', 'المدرسة': 'المدرسة',
    'الجامعة': 'الجامعة', 'المستشفى': 'المستشفى', 'المطار': 'المطار',
    
    # Adjectives
    'كبير': 'كبير', 'صغير': 'صغير', 'جديد': 'جديد', 'قديم': 'قديم',
    'حسن': 'حسن', 'جميل': 'جميل', 'قبيح': 'قبيح', 'طويل': 'طويل',
    'قصير': 'قصير', 'عريض': 'عريض', 'ضيق': 'ضيق', 'ثقيل': 'ثقيل',
    'خفيف': 'خفيف', 'سريع': 'سريع', 'بطيء': 'بطيء', 'حار': 'حار',
    'بارد': 'بارد', 'دافئ': 'دافئ',
    
    # Numbers
    'واحد': 'واحد', 'اثنان': 'اثنان', 'ثلاثة': 'ثلاثة', 'أربعة': 'أربعة',
    'خمسة': 'خمسة', 'ستة': 'ستة', 'سبعة': 'سبعة', 'ثمانية': 'ثمانية',
    'تسعة': 'تسعة', 'عشرة': 'عشرة', 'مئة': 'مئة', 'ألف': 'ألف',
    'مليون': 'مليون', 'مليار': 'مليار',
    
    # Demonstratives
    'هذا': 'هذا', 'هذه': 'هذه', 'هذان': 'هذان', 'هذين': 'هذين',
    'هؤلاء': 'هؤلاء', 'ذلك': 'ذلك', 'تلك': 'تلك', 'أولئك': 'أولئك',
    'هنا': 'هنا', 'هناك': 'هناك',
    
    # Question words
    'أين': 'أين', 'كيف': 'كيف', 'متى': 'متى', 'لماذا': 'لماذا',
    'هل': 'هل', 'ما': 'ما', 'من': 'من', 'أي': 'أي', 'كم': 'كم',
    
    # Time
    'اليوم': 'اليوم', 'أمس': 'أمس', 'غداً': 'غداً', 'الآن': 'الآن',
    'صباحاً': 'صباحاً', 'مساءً': 'مساءً', 'ليلاً': 'ليلاً',
    'الأسبوع': 'الأسبوع', 'الشهر': 'الشهر', 'السنة': 'السنة',
    
    # Common phrases
    'مرحبا': 'مرحبا', 'أهلا': 'أهلا', 'وداعا': 'وداعا', 'شكرا': 'شكرا',
    'عفوا': 'عفوا', 'نعم': 'نعم', 'لا': 'لا', 'بلى': 'بلى',
    'السلام': 'السلام', 'عليكم': 'عليكم', 'ورحمة': 'ورحمة', 'الله': 'الله',
    'وبركاته': 'وبركاته',
}


@register_tool('arabic_spell_checker')
class ArabicSpellChecker(BaseTool):
    """
    أداة فحص الإملاء العربي - تفحص النص العربي وتكتشف الأخطاء الإملائية المحتملة
    """
    
    description = 'أداة فحص الإملاء العربي - تفحص النص العربي وتكتشف الأخطاء الإملائية'
    parameters = [
        {
            'name': 'text',
            'type': 'string',
            'description': 'النص العربي المراد فحصه',
            'required': True
        },
        {
            'name': 'check_diacritics',
            'type': 'boolean',
            'description': 'فحص علامات التشكيل',
            'required': False,
            'default': True
        },
        {
            'name': 'suggest_corrections',
            'type': 'boolean',
            'description': 'اقتراح تصحيحات للأخطاء',
            'required': False,
            'default': True
        }
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.common_words = COMMON_ARABIC_WORDS
    
    def _normalize_arabic(self, text: str) -> str:
        """تطبيع النص العربي"""
        # Remove diacritics (tashkeel)
        arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670]')
        text = arabic_diacritics.sub('', text)
        
        # Normalize alef variants
        text = re.sub(r'[إأآٱ]', 'ا', text)
        
        # Normalize yaa
        text = re.sub(r'ى', 'ي', text)
        
        # Normalize taa marbouta
        text = re.sub(r'ة', 'ه', text)
        
        # Remove tatweel (kashida)
        text = re.sub(r'ـ', '', text)
        
        return text
    
    def _check_spelling(self, word: str) -> Dict:
        """فحص إملاء كلمة واحدة"""
        normalized = self._normalize_arabic(word)
        
        # Check if word is in common words dictionary
        if normalized in self.common_words:
            return {
                'word': word,
                'is_correct': True,
                'suggestion': None
            }
        
        # Basic length and character check
        if len(normalized) < 2:
            return {
                'word': word,
                'is_correct': True,  # Too short to judge
                'suggestion': None
            }
        
        # Check for non-Arabic characters
        arabic_pattern = re.compile(r'^[\u0600-\u06FF\s]+$')
        if not arabic_pattern.match(normalized):
            return {
                'word': word,
                'is_correct': False,
                'error_type': 'non_arabic',
                'suggestion': None
            }
        
        # Find similar words for suggestions
        suggestions = []
        for known_word in self.common_words:
            # Simple similarity check (same length or close)
            if abs(len(normalized) - len(known_word)) <= 2:
                # Check for common substrings
                if normalized[:2] == known_word[:2]:
                    suggestions.append(known_word)
        
        return {
            'word': word,
            'is_correct': False,
            'error_type': 'unknown_word',
            'suggestion': suggestions[:3] if suggestions else None
        }
    
    def _check_diacritics(self, text: str) -> List[Dict]:
        """فحص علامات التشكيل"""
        issues = []
        
        # Check for common diacritic issues
        diacritic_pattern = re.compile(r'[\u064B-\u065F\u0670]')
        
        # If text has no diacritics, it's okay (modern Arabic often omits them)
        # But we can check for common patterns
        
        return issues
    
    def call(self, params: str, **kwargs) -> str:
        """فحص النص العربي"""
        import json5
        params = json5.loads(params)
        
        text = params.get('text', '')
        check_diacritics = params.get('check_diacritics', True)
        suggest_corrections = params.get('suggest_corrections', True)
        
        if not text:
            return json.dumps({
                'success': False,
                'error': 'يرجى توفير النص للفحص'
            }, ensure_ascii=False)
        
        try:
            # Split text into words (preserve punctuation)
            words = re.findall(r'[\u0600-\u06FF]+', text)
            
            if not words:
                return json.dumps({
                    'success': True,
                    'text': text,
                    'is_correct': True,
                    'message': 'لم يتم العثور على كلمات عربية للفحص',
                    'errors': []
                }, ensure_ascii=False)
            
            # Check each word
            errors = []
            for word in words:
                result = self._check_spelling(word)
                if not result['is_correct']:
                    errors.append(result)
            
            # Check diacritics if requested
            diacritic_issues = []
            if check_diacritics:
                diacritic_issues = self._check_diacritics(text)
            
            # Prepare response
            response = {
                'success': True,
                'text': text,
                'is_correct': len(errors) == 0 and len(diacritic_issues) == 0,
                'total_words': len(words),
                'error_count': len(errors),
                'errors': errors if suggest_corrections else [],
                'diacritic_issues': diacritic_issues,
                'message': 'النص صحيح' if len(errors) == 0 else f'تم العثور على {len(errors)} أخطاء'
            }
            
            return json.dumps(response, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)


@register_tool('arabic_text_normalizer')
class ArabicTextNormalizer(BaseTool):
    """
    أداة تطبيع النصوص العربية - إزالة التشكيل وتوحيد الحروف
    """
    
    description = 'أداة تطبيع النصوص العربية - إزالة التشكيل وتوحيد الحروف العربية'
    parameters = [
        {
            'name': 'text',
            'type': 'string',
            'description': 'النص العربي المراد تطبيعه',
            'required': True
        },
        {
            'name': 'remove_diacritics',
            'type': 'boolean',
            'description': 'إزالة علامات التشكيل',
            'required': False,
            'default': True
        },
        {
            'name': 'normalize_alef',
            'type': 'boolean',
            'description': 'توحيد الحرف Alef (أ إ آ → ا)',
            'required': False,
            'default': True
        },
        {
            'name': 'normalize_yaa',
            'type': 'boolean',
            'description': 'توحيد الحرف Yaa (ى → ي)',
            'required': False,
            'default': True
        },
        {
            'name': 'remove_kashida',
            'type': 'boolean',
            'description': 'إزالة التطويل (ـ)',
            'required': False,
            'default': True
        }
    ]
    
    def call(self, params: str, **kwargs) -> str:
        """تطبيع النص العربي"""
        import json5
        params = json5.loads(params)
        
        text = params.get('text', '')
        remove_diacritics = params.get('remove_diacritics', True)
        normalize_alef = params.get('normalize_alef', True)
        normalize_yaa = params.get('normalize_yaa', True)
        remove_kashida = params.get('remove_kashida', True)
        
        if not text:
            return json.dumps({
                'success': False,
                'error': 'يرجى توفير النص للتطبيع'
            }, ensure_ascii=False)
        
        try:
            original_text = text
            
            # Remove diacritics
            if remove_diacritics:
                arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670]')
                text = arabic_diacritics.sub('', text)
            
            # Normalize alef
            if normalize_alef:
                text = re.sub(r'[إأآٱ]', 'ا', text)
            
            # Normalize yaa
            if normalize_yaa:
                text = re.sub(r'ى', 'ي', text)
            
            # Remove kashida
            if remove_kashida:
                text = re.sub(r'ـ', '', text)
            
            return json.dumps({
                'success': True,
                'original': original_text,
                'normalized': text,
                'changes': {
                    'diacritics_removed': remove_diacritics,
                    'alef_normalized': normalize_alef,
                    'yaa_normalized': normalize_yaa,
                    'kashida_removed': remove_kashida
                }
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'success': False,
                'error': str(e)
            }, ensure_ascii=False)
