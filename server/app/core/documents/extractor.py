from pathlib import Path
from pypdf import PdfReader


class PDFTextExtractor:
    def extract(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists(file_path):
            raise FileNotFoundError(f"pdf file not found:{file_path}")

        reader = PdfReader(str(path))
        pages: list[str] = []
        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)
