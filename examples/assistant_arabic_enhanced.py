#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example of using Qwen-Agent with Arabic language support and enhanced tools.

This example demonstrates:
1. Using the Assistant agent with Arabic language support
2. Using the new TextToSpeech tool to convert Arabic text to speech
3. Using the ArabicTextProcessor tool to process and normalize Arabic text
4. Running the agent with Arabic prompts
"""

import pprint
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print


def main():
    # Configure the LLM
    llm_cfg = {
        # Using DashScope API
        'model': 'qwen-max-latest',
        'model_type': 'qwen_dashscope',
        # 'api_key': 'YOUR_DASHSCOPE_API_KEY',
        # It will use the DASHSCOPE_API_KEY environment variable if not set here
        
        # Or use a local model service compatible with OpenAI API:
        # 'model': 'Qwen2.5-7B-Instruct',
        # 'model_server': 'http://localhost:8000/v1',
        # 'api_key': 'EMPTY',
        
        'generate_cfg': {
            'top_p': 0.8
        }
    }

    # Create an assistant with Arabic language support
    system_instruction = '''أنت مساعد ذكي يتحدث اللغة العربية بطلاقة.
يمكنك:
- الإجابة على الأسئلة بالعربية
- تحويل النصوص إلى كلام
- معالجة ومعالجة النصوص العربية
- تقديم معلومات مفيدة وموثوقة

يرجى الرد دائماً باللغة العربية.'''

    # Define the tools to use
    tools = [
        'text_to_speech',  # Convert Arabic text to speech
        'arabic_text_processor',  # Process and normalize Arabic text
        'code_interpreter',  # Execute code if needed
    ]

    # Create the assistant
    bot = Assistant(
        llm=llm_cfg,
        system_message=system_instruction,
        function_list=tools,
        name='مساعد قوي',
        description='مساعد ذكي يدعم اللغة العربية بشكل كامل'
    )

    # Run the chatbot
    messages = []
    print("مرحباً! أنا مساعدك الذكي. يمكنك أن تسأل أي سؤال بالعربية.")
    print("اكتب 'خروج' للإنهاء.\n")

    while True:
        # Get user input
        query = input('أنت: ')
        
        if query.lower() in ['خروج', 'exit', 'quit']:
            print("شكراً لاستخدامك المساعد. إلى اللقاء!")
            break
        
        # Add user message to history
        messages.append({'role': 'user', 'content': query})
        
        # Get bot response
        response = []
        response_plain_text = ''
        print('المساعد: ')
        
        try:
            for response in bot.run(messages=messages, lang='ar'):
                # Stream the response
                response_plain_text = typewriter_print(response, response_plain_text)
        except Exception as e:
            print(f"خطأ: {str(e)}")
            continue
        
        # Add bot response to history
        messages.extend(response)
        print('\n')


def example_with_gui():
    """Example of running the assistant with a web UI."""
    from qwen_agent.gui import WebUI
    
    llm_cfg = {
        'model': 'qwen-max-latest',
        'model_type': 'qwen_dashscope',
    }

    system_instruction = '''أنت مساعد ذكي يتحدث اللغة العربية بطلاقة.
يمكنك الإجابة على الأسئلة وتقديم معلومات مفيدة.'''

    tools = [
        'text_to_speech',
        'arabic_text_processor',
        'code_interpreter',
    ]

    bot = Assistant(
        llm=llm_cfg,
        system_message=system_instruction,
        function_list=tools,
        name='مساعد قوي',
        description='مساعد ذكي يدعم اللغة العربية'
    )

    # Configure the chatbot UI
    chatbot_config = {
        'user.name': 'أنت',
        'agent.avatar': 'qwen',
        'input.placeholder': 'اسأل أي سؤال بالعربية...',
        'prompt.suggestions': [
            'ما هي اللغة العربية؟',
            'اشرح لي الذكاء الاصطناعي',
            'كيف يمكنني تحسين مهاراتي في البرمجة؟',
        ]
    }

    # Launch the web UI
    ui = WebUI(bot, chatbot_config=chatbot_config)
    ui.run(server_name='0.0.0.0', server_port=7860)


if __name__ == '__main__':
    # Run the command-line chatbot
    main()
    
    # Uncomment the following line to run with GUI instead
    # example_with_gui()
