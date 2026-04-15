from datetime import datetime

metricas_data = []

def registrar_evento(tipo):
    metricas_data.append({
        "tipo": tipo,
        "timestamp": datetime.utcnow().isoformat()
    })

def obtener_metricas():
    return metricas_data