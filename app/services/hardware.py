import pandas as pd
from thefuzz import process, fuzz
import os

dir_data = os.path.join(os.path.dirname(__file__), '../../data')

def carregar_csv(nome):
    df = pd.read_csv(os.path.join(dir_data, nome))
    return dict(zip(df['Name'], df['Score']))

cpu_scores = carregar_csv('cpus_com_scores.csv')
gpu_scores = carregar_csv('gpus_com_scores.csv')

def classificar_performance(score_user, score_req):
    razao = score_user / score_req
    
    if razao >= 2.0:
        return 4, "RODA NO ULTRA 🚀", True
    elif razao >= 1.0:
        return 3, "RODA LISO 🎮", True
    elif razao >= 0.75:
        return 2, "RODA SOFRENDO 🟡", True 
    else:
        return 1, "NÃO RODA NEM A PAU 🔴", False

def calcular_veredicto(cpu_user, gpu_user, cpu_req_txt, gpu_req_txt):
    match_cpu, _ = process.extractOne(cpu_req_txt, list(cpu_scores.keys()), scorer=fuzz.token_set_ratio)
    match_gpu, _ = process.extractOne(gpu_req_txt, list(gpu_scores.keys()), scorer=fuzz.token_set_ratio)
    
    s_cpu_req = cpu_scores[match_cpu]
    s_gpu_req = gpu_scores[match_gpu]
    s_cpu_user = cpu_scores[cpu_user]
    s_gpu_user = gpu_scores[gpu_user]
    
    nivel_cpu, msg_cpu, pass_cpu = classificar_performance(s_cpu_user, s_cpu_req)
    nivel_gpu, msg_gpu, pass_gpu = classificar_performance(s_gpu_user, s_gpu_req)
    
    nivel_final = min(nivel_cpu, nivel_gpu)
    
    mensagens = {
        4: "RODA NO ULTRA! 🚀🤯",
        3: "RODA LISO! 🎮✨",
        2: "RODA SOFRENDO! 🟡 (720p no Low)",
        1: "NÃO RODA NEM A PAU! 🔴😭"
    }
    
    return {
        "veredicto_final": mensagens[nivel_final],
        "nivel": nivel_final,
        "cpu": {"passou": pass_cpu, "score_exigido": int(s_cpu_req), "peca": match_cpu, "status": msg_cpu},
        "gpu": {"passou": pass_gpu, "score_exigido": int(s_gpu_req), "peca": match_gpu, "status": msg_gpu}
    }