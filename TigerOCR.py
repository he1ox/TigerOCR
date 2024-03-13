import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import io
import tempfile
import matplotlib.pyplot as plt
from collections import Counter

import pyperclip
from database import connection as db_mongo
from fields import select_fields as fields 
from pdf import gen_pdf as pdf
from pdf import convert as convert_pdf
# Configurar el comando de Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_image(image):
    return pytesseract.image_to_string(image, lang="eng")


def read_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # images = convert_from_path(temp_file_path, poppler_path=r"C:\Py_Projects\poppler-24.02.0\Library\bin")
    images = convert_from_path(temp_file_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image, lang="eng")

    return text


def plot_word_frequency(text, num_words=10):
    words = text.split()
    word_counts = Counter(words)
    common_words = word_counts.most_common(num_words)

    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.title("Top Palabras Más Frecuentes")
    st.pyplot(plt)
    
def show_pdf(pdf_path):
    imagenes = convert_pdf.toImage(pdf_path)
    for imagen in imagenes:
        st.image(imagen, caption="Imagen cargada", use_column_width=True)


# Base de datos
db_mongo.get_Connection()

st.markdown(
    """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>
    """,
    unsafe_allow_html=True,
)

st.title("OCR - Dev Tigers 🐯")
st.caption(
    "¡Da vida a tus documentos con OCR - Tigers! Nuestra aplicación no solo convierte archivos PDF, PNG, JPEG y BMP en texto editable, sino que también ofrece un análisis detallado de la frecuencia de palabras. Simplifica la digitalización de tus documentos y obtén insights valiosos con OCR - Tigers."
)

# Barra lateral para configuraciones adicionales
st.sidebar.title("Configuración")
languages = ["English", "Español"]  # Puedes añadir más idiomas
selected_lang = st.sidebar.selectbox("Selecciona el idioma para OCR", languages)


uploaded_file = st.file_uploader(
    "Seleccionar un archivo 📁 (PDF, PNG, JPEG, BMP)",
    type=["pdf", "png", "jpeg", "bmp"],
)

if uploaded_file is not None:

    with st.spinner("Procesando..."):
        if uploaded_file.type == "application/pdf":
            text = read_pdf(uploaded_file)

        else:
            image = Image.open(uploaded_file)
            text = read_image(image)
            st.image(image, caption="Imagen cargada", use_column_width=True)

    st.success("Procesamiento completado!")

    st.write("Texto extraído:")
    dict_fields = fields.getImportantFields(text)
    
    if st.button("Generar PDF", type="primary"):
        pdf_filename = pdf.build(dict_fields)
        show_pdf(pdf_filename)
        st.success(f"PDF generado: {pdf_filename}")
    if st.button("Copiar", type="secondary"):
        
        db_mongo.createDataUser(dict_fields)
        pyperclip.copy(str(dict_fields))
        # Todo: Eliminar cuando se terminen las pruebas
        st.text_area("", str(dict_fields), height=300)
        st.success("Texto copiado al portapapeles!")

    st.text_area("", text, height=300)
    if st.button("Mostrar Análisis de Frecuencia de Palabras"):
        plot_word_frequency(text)
