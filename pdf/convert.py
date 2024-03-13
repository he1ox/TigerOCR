import fitz
from PIL import Image

def toImage(pdf_path):
    imagenes = []
    pdf_doc = fitz.open(pdf_path)
    print(f'Número de páginas: {pdf_doc.page_count}')
    for pagina in range(pdf_doc.page_count):
        pagina = pdf_doc.load_page(pagina)
        imagen= pagina.get_pixmap()
        imagen_pil = Image.frombytes("RGB", [imagen.width, imagen.height], imagen.samples)
        imagenes.append(imagen_pil)
    return imagenes

