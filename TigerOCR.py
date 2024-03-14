from io import BytesIO
import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
import matplotlib.pyplot as plt
from collections import Counter

import os
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


def generate_pdf():
    pass


# Base de datos
db_mongo.get_Connection()

st.markdown(
    """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>
    """,
    unsafe_allow_html=True,
)

st.title("TechDocAdvantage PRO")
st.caption(
    "¡Da vida a tus documentos con TechDocAdvantage PRO! Nuestra aplicación no solo convierte archivos PDF, PNG y JPEG. Simplifica la digitalización de tus documentos y obtén insights valiosos con TechDocAdvantage PRO."
)


uploaded_file = st.file_uploader(
    "Seleccionar un archivo 📁 (PDF, PNG, JPEG)",
    type=["pdf", "png", "jpeg"],
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
    st.text_area("", text, height=300)

    dict_fields = fields.getImportantFields(text)
    pdf_filename = None

    transform_data = pdf.transform(dict_fields)
    tabla_datos = [transform_data]

    st.table(tabla_datos)

    if st.button("Guardar Información"):

        db_mongo.createDataUser(dict_fields)

        uploaded_file.seek(0)

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        pdf_path = "temp.pdf"
        img = convert_pdf.toImage(pdf_path)

        with open("temp.jpg", "wb") as f:
            img[0].save(f, "JPEG")
        img = "temp.jpg"

        field_id = db_mongo.saveImage(img, dict_fields["nis"])

        st.image(img, caption="Imagen guardada", use_column_width=True)
        st.success("Datos guardados en la base de datos")
        os.remove(img)
        os.remove(pdf_path)

    # Generar el pdf y poner el boton de descargar
    # TODO: Cargar datos de los todos los usuarios en tablas de streamlit
    # TODO: Agregar el boton para visualizar la imagen
    if st.button("Generar PDF", type="secondary"):

        with st.spinner("Generando PDF..."):
            pdf_filename = pdf.build(dict_fields)

            show_pdf(pdf_filename)
        st.success(f"PDF generado: {pdf_filename}")

        with open(pdf_filename, "rb") as f:
            bytes = f.read()

        st.download_button(
            "Descargar PDF",
            bytes,
            file_name="factura01.pdf",
            mime="application/pdf",
        )
        os.remove(pdf_filename)

# TODO: Unir todos los usuarios y mostrar la imagen de energuate cargada en mongo
st.success("Información general de recibos de luz")
users = db_mongo.getAllUsers()

for user in users:
    new_data = pdf.transform(user)
    st.table([new_data])
