from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def transform(data: dict[str, str]):

    data["consumption_kwh"] = f'{data["consumption_kwh"]} kWh'
    data["public_light"] = f'Q.{data["public_light"]}'
    data["total_pay"] = f'Q.{data["total_pay"]}'

    label = {
        "nis": "NIS",
        "date_issue": "Fecha de Emisión",
        "consumption_kwh": "Consumo de Electricidad",
        "public_light": "Tasa de Alumbrado Público",
        "start_period": "Periodo de Inicio",
        "end_period": "Periodo de Fin",
        "total_pay": "Total a Pagar",
    }

    return {label[key]: value for key, value in data.items()}


def build(data: dict[str, str]):
    data = transform(data)
    print(f"{data=}")
    pdf_filename = "output.pdf"
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

    data = [[str(key), str(value)] for key, value in data.items()]
    print(f"{data=}")

    table = Table(data)

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table.setStyle(style)

    content = []
    content.append(table)

    pdf.build(content)

    return pdf_filename
