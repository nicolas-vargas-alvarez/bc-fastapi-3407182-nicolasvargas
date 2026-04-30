from fastapi import FastAPI, HTTPException

# ============================================
# CONFIGURACIÓN
# ============================================

MESSAGES: dict[str, str] = {
    "es": "Hola {name}, gracias por contactar nuestro call center.",
    "en": "Hello {name}, thank you for contacting our call center.",
    "fr": "Bonjour {name}, merci de contacter notre centre d'appels.",
}

SUPPORTED_LANGUAGES = list(MESSAGES.keys())

# ============================================
# APP
# ============================================

app = FastAPI(
    title="Call Center API",
    description="API para gestión básica de atención en call center",
    version="1.0.0"
)

# ============================================
# RF-01: INFO API
# ============================================

@app.get("/")
async def root() -> dict[str, str]:
    """Información de la API del call center."""
    return {
        "name": "Call Center API",
        "version": "1.0.0",
        "domain": "call-center"
    }

# ============================================
# RF-02: BIENVENIDA
# ============================================

@app.get("/agent/{name}")
async def welcome_agent(
    name: str,
    language: str = "es"
) -> dict[str, str]:
    """Bienvenida personalizada para clientes del call center."""

    template = MESSAGES.get(language, MESSAGES["es"])
    message = template.format(name=name)

    return {
        "message": message,
        "agent": name,
        "language": language if language in MESSAGES else "es"
    }

# ============================================
# RF-03: INFORMACIÓN DE LLAMADA
# ============================================

@app.get("/call/{call_id}/info")
async def call_info(
    call_id: str,
    detail_level: str = "basic"
) -> dict:
    """Información de una llamada del sistema."""

    basic_info = {
        "call_id": call_id,
        "status": "en curso",
        "agent": "Carlos Pérez"
    }

    if detail_level == "full":
        basic_info.update({
            "duration": "5 minutos",
            "client": "Juan López",
            "department": "soporte técnico"
        })

    return basic_info

# ============================================
# RF-04: SERVICIO SEGÚN HORARIO
# ============================================

@app.get("/service/schedule")
async def service_schedule(hour: int) -> dict:
    """Disponibilidad del call center según la hora."""

    if hour < 0 or hour > 23:
        raise HTTPException(status_code=400, detail="Hora inválida (0-23)")

    if 6 <= hour <= 11:
        return {
            "message": "Turno mañana - Atención al cliente activa",
            "available": ["soporte", "ventas"]
        }
    elif 12 <= hour <= 17:
        return {
            "message": "Turno tarde - Alto tráfico de llamadas",
            "available": ["soporte", "facturación"]
        }
    else:
        return {
            "message": "Turno noche - Servicio reducido",
            "available": ["soporte básico"]
        }

# ============================================
# RF-05: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Estado de la API."""
    return {
        "status": "healthy",
        "domain": "call-center"
    }