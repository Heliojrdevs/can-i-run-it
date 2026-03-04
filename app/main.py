from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schema import ConsultaHardware
from app.services.steam import buscar_dados_jogo, extrair_requisitos, buscar_jogos_por_nome
from app.services.hardware import calcular_veredicto, cpu_scores, gpu_scores

app = FastAPI(title="API - Can I Run It")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/listar-pecas")
def listar():
    return {"cpus": list(cpu_scores.keys()), "gpus": list(gpu_scores.keys())}

@app.get("/buscar-jogo-steam")
def buscar_jogo(nome: str):
    return buscar_jogos_por_nome(nome)

@app.post("/verificar-jogo")
def verificar(req: ConsultaHardware):
    jogo = buscar_dados_jogo(req.app_id_steam)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
        
    cpu_req_t, gpu_req_t = extrair_requisitos(jogo['texto_requisitos'])
    res = calcular_veredicto(req.cpu_usuario, req.gpu_usuario, cpu_req_t, gpu_req_t)
    res["jogo"] = jogo['nome']
    
    return res