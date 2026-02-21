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

import os
import re
from typing import List, Union

from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.utils import logger

# Try to import necessary libraries for document parsing
try:
    from pypdf import PdfReader
except ImportError:
    logger.info("pypdf not found, installing...")
    os.system("pip install pypdf")
    from pypdf import PdfReader

try:
    from docx import Document
except ImportError:
    logger.info("python-docx not found, installing...")
    os.system("pip install python-docx")
    from docx import Document


@register_tool("arabic_doc_parser")
class ArabicDocParser(BaseTool):
    """
    A tool for parsing and extracting text from Arabic documents (PDF, DOCX, TXT).
    It includes basic Arabic text cleaning and chunking capabilities.
    """

    description = (
        "Parse and extract text from Arabic documents (PDF, DOCX, TXT). "
        "Includes basic Arabic text cleaning and chunking for RAG purposes."
    )
    parameters = [
        {
            "name": "file_path",
            "type": "string",
            "description": "The path to the Arabic document file (PDF, DOCX, or TXT).",
            "required": True,
        },
        {
            "name": "chunk_size",
            "type": "integer",
            "description": "Maximum number of characters per text chunk. Defaults to 500.",
            "required": False,
        },
        {
            "name": "overlap",
            "type": "integer",
            "description": "Number of characters to overlap between chunks. Defaults to 50.",
            "required": False,
        },
    ]

    def call(self, params: Union[str, dict], **kwargs) -> List[str]:
        params = self._verify_json_format_args(params)
        file_path = params["file_path"]
        chunk_size = params.get("chunk_size", 500)
        overlap = params.get("overlap", 50)

        if not os.path.exists(file_path):
            return [f"Error: File not found at {file_path}"]

        file_extension = os.path.splitext(file_path)[1].lower()
        text = ""

        try:
            if file_extension == ".pdf":
                text = self._extract_text_from_pdf(file_path)
            elif file_extension == ".docx":
                text = self._extract_text_from_docx(file_path)
            elif file_extension == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                return [f"Error: Unsupported file type: {file_extension}"]
        except Exception as e:
            return [f"Error extracting text from {file_path}: {str(e)}"]

        cleaned_text = self._clean_arabic_text(text)
        chunks = self._chunk_text(cleaned_text, chunk_size, overlap)
        return chunks

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def _extract_text_from_docx(self, docx_path: str) -> str:
        document = Document(docx_path)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _clean_arabic_text(self, text: str) -> str:
        # Remove extra spaces and normalize common Arabic characters
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"[أإآ]", "ا", text)  # Normalize Alef variants
        text = re.sub(r"ة", "ه", text)    # Normalize Teh Marbuta
        text = re.sub(r"[ىي]", "ي", text)    # Normalize Yeh variants
        return text

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
            if start < 0: # Handle cases where chunk_size - overlap is negative
                start = 0
        return chunks
