import re

nis = re.compile(r"NIS: (\d+)")
fecha_emision = re.compile(r"Fecha de Emisién: (\d{2}/\d{2}/\d{4})")
consumo_electricidad = re.compile(r"Consumo de Electricidad (\d+) KWh")
alumbrado_publico = re.compile(
    r"(\d{1,4}(?:,\d{3})*(?:\.\d{2})?) Tasa de Alumbrado Publico"
)
periodo_lectura = re.compile(
    r"PERIODO DE LECTURA: (\d{2}/\d{2}/202[0-9]{1}) al (\d{2}/\d{2}/202[0-9]{1})"
)
pagar = re.compile(r"TOTAL Q (\d{1,4}(?:,\d{3})*(?:\.\d{2})?)")


def getImportantFields(text) -> dict[str, str]:
    nit_match = re.search(nis, text)
    date_match = re.search(fecha_emision, text)
    consumption_match = re.search(consumo_electricidad, text)
    public_light_match = re.search(alumbrado_publico, text)
    reading_period_match = re.search(periodo_lectura, text)
    total_match = re.search(pagar, text)

    nit = nit_match.group(1) if nit_match else "NIT no encontrado"
    date = date_match.group(1) if date_match else "Fecha no encontrada"
    consumption = (
        consumption_match.group(1) if consumption_match else "Consumo no encontrado"
    )
    public_light = (
        public_light_match.group(1)
        if public_light_match
        else "Tasa de alumbrado no encontrada"
    )
    reading_period = (
        reading_period_match.group(1)
        if reading_period_match
        else "Periodo de lectura no encontrado"
    )

    end_period = (
        reading_period_match.group(2)
        if reading_period_match
        else "Periodo de lectura no encontrado"
    )

    total = total_match.group(1) if total_match else "Total no encontrado"

    return {
        "nis": nit,
        "date_issue": date,
        "consumption_kwh": consumption,
        "public_light": public_light,
        "start_period": reading_period,
        "end_period": end_period,
        "total_pay": total,
    }
