from pydantic import BaseModel

class ConsultaHardware(BaseModel):
    cpu_usuario: str
    gpu_usuario: str
    app_id_steam: str