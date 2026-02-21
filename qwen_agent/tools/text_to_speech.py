import os
import urllib.parse
from typing import Union

from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.utils import logger

@register_tool('text_to_speech')
class TextToSpeech(BaseTool):
    description = 'Convert text to speech audio file. Input the text to be spoken, and it returns the path to the generated audio file.'
    parameters = [{
        'name': 'text',
        'type': 'string',
        'description': 'The text to convert to speech',
        'required': True
    }, {
        'name': 'lang',
        'type': 'string',
        'description': 'The language code (e.g., "en" for English, "ar" for Arabic)',
        'required': False
    }]

    def call(self, params: Union[str, dict], **kwargs) -> str:
        params = self._verify_json_format_args(params)
        text = params['text']
        lang = params.get('lang', 'ar')  # Default to Arabic as per user preference

        try:
            from gtts import gTTS
        except ImportError:
            logger.info('Installing gTTS...')
            os.system('pip install gTTS')
            from gtts import gTTS

        try:
            tts = gTTS(text=text, lang=lang)
            
            # Create a directory for outputs if it doesn't exist
            output_dir = os.path.join(os.getcwd(), 'outputs', 'audio')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate a filename based on text hash or just a simple counter/timestamp
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
            file_path = os.path.join(output_dir, f'tts_{text_hash}.mp3')
            
            tts.save(file_path)
            
            # Return the file path in a format the agent can recognize
            return f'Audio file generated at: {file_path}'
        except Exception as e:
            return f'Error generating speech: {str(e)}'
