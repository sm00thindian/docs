import docx
from docx.shared import Inches
from abc import ABC, abstractmethod
from PIL import Image
import io
import easyocr

class DocumentIngester(ABC):
    """Base class for document ingesters. Extend for new file types."""
    
    @abstractmethod
    def ingest(self, file_path: str, **kwargs) -> str:
        """Ingest the document and return raw text."""
        pass

class WordDocumentIngester(DocumentIngester):
    """Ingester for .docx files."""
    
    def __init__(self):
        self.ocr_reader = None
    
    def ingest(self, file_path: str, ocr_images: bool = False) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = []
            
            # Extract text from paragraphs
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            # Optionally detect and extract text from images (inline shapes)
            if ocr_images:
                # Initialize EasyOCR reader (English only, CPU for portability)
                if self.ocr_reader is None:
                    self.ocr_reader = easyocr.Reader(['en'], gpu=False)
                
                for shape in doc.inline_shapes:
                    if shape.type == docx.enum.shape.WD_INLINE_SHAPE.PICTURE:
                        # Get the image blob
                        rel = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                        image_part = doc.part.related_to(rel, docx.opc.constants.RELATIONSHIP_TYPE.IMAGE)
                        image_blob = image_part.blob
                        
                        # Open image with Pillow
                        image = Image.open(io.BytesIO(image_blob))
                        
                        # Perform OCR with EasyOCR
                        ocr_results = self.ocr_reader.readtext(image, detail=0)  # detail=0 returns text only
                        ocr_text = ' '.join(ocr_results).strip()
                        
                        # Append OCR text if any, with a marker
                        if ocr_text:
                            full_text.append(f"[Image Text: {ocr_text}]")
            
            return '\n'.join(full_text)
        except Exception as e:
            raise ValueError(f"Error ingesting {file_path}: {e}")
