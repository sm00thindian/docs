# src/ingestion.py
import docx
from abc import ABC, abstractmethod
from PIL import Image
import io
import easyocr
import numpy as np
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO)

class DocumentIngester(ABC):
    @abstractmethod
    def ingest(self, file_path: str, **kwargs) -> str:
        pass

class WordDocumentIngester(DocumentIngester):
    def __init__(self):
        self.ocr_reader: Optional[easyocr.Reader] = None
        self._ocr_lock = False  # Prevent multiple init

    def _init_ocr(self):
        if self.ocr_reader is None and not self._ocr_lock:
            self._ocr_lock = True
            logging.info("Initializing EasyOCR (CPU, batched)...")
            self.ocr_reader = easyocr.Reader(['en'], gpu=False, recognizer=True, detector=True)
            self._ocr_lock = False

    def ingest(self, file_path: str, ocr_images: bool = False) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text.strip()]
            
            if ocr_images and doc.inline_shapes:
                self._init_ocr()
                images = []
                for shape in doc.inline_shapes:
                    if shape.type != docx.enum.shape.WD_INLINE_SHAPE.PICTURE:
                        continue
                    try:
                        rel = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                        if not rel:
                            continue
                        image_part = doc.part.related_parts.get(rel)
                        if not image_part:
                            continue
                        blob = image_part.blob
                        img = Image.open(io.BytesIO(blob)).convert('RGB')
                        images.append(np.array(img))
                    except Exception as e:
                        logging.debug(f"Image load failed: {e}")

                if images:
                    # Batch OCR
                    try:
                        results = self.ocr_reader.readtext_batched(
                            images,
                            detail=0,
                            allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,;:!?-()[]{}"\'/\\@#$%&*+=<>',
                            batch_size=8
                        )
                        for text in results:
                            if text := text.strip():
                                full_text.append(f"[Image Text: {text}]")
                    except Exception as e:
                        logging.warning(f"Batch OCR failed, falling back: {e}")
                        # Fallback per image
                        for img in images:
                            try:
                                text = ' '.join(self.ocr_reader.readtext(img, detail=0)).strip()
                                if text:
                                    full_text.append(f"[Image Text: {text}]")
                            except:
                                full_text.append("[Image: OCR failed]")

            return '\n'.join(full_text)
        except Exception as e:
            raise ValueError(f"Error ingesting {file_path}: {e}")
