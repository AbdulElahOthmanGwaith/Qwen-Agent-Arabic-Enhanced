# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import Union

from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.utils import logger


@register_tool('arabic_text_processor')
class ArabicTextProcessor(BaseTool):
    """
    A tool for processing and normalizing Arabic text.
    Handles diacritics removal, text normalization, and other Arabic-specific operations.
    """
    
    description = 'Process and normalize Arabic text. Removes diacritics, normalizes text, and handles Arabic-specific operations.'
    parameters = [{
        'name': 'text',
        'type': 'string',
        'description': 'The Arabic text to process',
        'required': True
    }, {
        'name': 'operation',
        'type': 'string',
        'description': 'The operation to perform: "remove_diacritics", "normalize", "extract_keywords"',
        'required': False
    }]

    # Arabic diacritics
    ARABIC_DIACRITICS = re.compile(r'[\u064B-\u065F]')
    
    # Common Arabic stop words
    ARABIC_STOPWORDS = {
        'في', 'من', 'إلى', 'هذا', 'ذلك', 'التي', 'الذي', 'هو', 'هي',
        'أن', 'إن', 'كان', 'كانت', 'ليس', 'ليست', 'و', 'أو', 'لكن',
        'لم', 'لن', 'قد', 'كل', 'بعض', 'أي', 'أين', 'متى', 'كيف',
        'ماذا', 'من', 'ما', 'هنا', 'هناك', 'هنالك', 'الآن', 'اليوم',
        'أمس', 'غدا', 'الأمس', 'الغد', 'دائما', 'أبدا', 'أحيانا'
    }

    def call(self, params: Union[str, dict], **kwargs) -> str:
        params = self._verify_json_format_args(params)
        text = params.get('text', '')
        operation = params.get('operation', 'normalize')

        try:
            if operation == 'remove_diacritics':
                result = self._remove_diacritics(text)
            elif operation == 'normalize':
                result = self._normalize_text(text)
            elif operation == 'extract_keywords':
                result = self._extract_keywords(text)
            else:
                result = f'Unknown operation: {operation}. Supported operations: remove_diacritics, normalize, extract_keywords'
            
            return result
        except Exception as e:
            logger.error(f'Error processing Arabic text: {str(e)}')
            return f'Error processing text: {str(e)}'

    def _remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritical marks from text."""
        return self.ARABIC_DIACRITICS.sub('', text)

    def _normalize_text(self, text: str) -> str:
        """Normalize Arabic text by removing diacritics and standardizing characters."""
        # Remove diacritics
        text = self._remove_diacritics(text)
        
        # Normalize alef variations
        text = re.sub(r'[أإآ]', 'ا', text)
        
        # Normalize teh variations
        text = re.sub(r'ة', 'ه', text)
        
        # Normalize yeh variations
        text = re.sub(r'[ىي]', 'ي', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def _extract_keywords(self, text: str) -> str:
        """Extract keywords from Arabic text by removing stopwords."""
        # Normalize text first
        text = self._normalize_text(text)
        
        # Split into words
        words = text.split()
        
        # Filter out stopwords and short words
        keywords = [w for w in words if w not in self.ARABIC_STOPWORDS and len(w) > 2]
        
        # Return as JSON-like string
        import json
        return json.dumps({
            'keywords': keywords,
            'count': len(keywords),
            'original_word_count': len(words)
        }, ensure_ascii=False, indent=2)
