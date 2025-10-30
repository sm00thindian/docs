# src/ingestion.py
import docx
from docx.shared import Inches
from abc import ABC, abstractmethod
from PIL import Image
import io
import easyocr
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


class DocumentIngester(ABC):
    @abstractmethod
    def ingest(self, file_path: str, **kwargs) -> str:
        pass


class WordDocumentIngester(DocumentIngester):
    def __init__(self):
        self.ocr_reader = None
    
    def ingest(self, file_path: str, ocr_images: bool = False) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            
            if ocr_images:
                if self.ocr_reader is None:
                    logging.info("Initializing EasyOCR reader (CPU mode)...")
                    self.ocr_reader = easyocr.Reader(['en'], gpu=False)
                
                for shape in doc.inline_shapes:
                    if shape.type != docx.enum.shape.WD_INLINE_SHAPE.PICTURE:
                        continue

                    try:
                        rel = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                        if not rel:
                            continue
                        image_part = doc.part.related_parts[rel]
                        image_blob = image_part.blob

                        # Convert blob to numpy array
                        image = Image.open(io.BytesIO(image_blob)).convert('RGB')
                        image_np = np.array(image)

                        # OCR with allowlist and error handling
                        ocr_results = self.ocr_reader.readtext(
                            image_np,
                            detail=0,
                            allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,;:!?-()[]{}"\''
                        )
                        ocr_text = ' '.join(ocr_results).strip()
                        if ocr_text:
                            full_text.append(f"[Image Text: {ocr_text}]")
                    except Exception as e:
                        logging.warning(f"OCR failed on image in {file_path}: {e}")
                        full_text.append("[Image: OCR failed]")
            
            return '\n'.join(full_text)
        except Exception as e:
            raise ValueError(f"Error ingesting {file_path}: {e}")
