import requests
from bs4 import BeautifulSoup
import re

def buscar_dados_jogo(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    res = requests.get(url).json()
    
    if not res or str(app_id) not in res or not res[str(app_id)]['success']:
        return None
        
    data = res[str(app_id)]['data']
    html_req = data['pc_requirements'].get('minimum', '')
    texto = BeautifulSoup(html_req, "html.parser").get_text(separator=' ')
    
    return {"nome": data['name'], "texto_requisitos": texto}

def extrair_requisitos(texto_puro):
    m_cpu = re.search(r'(?:Processor|Processador):\s*(.*?)(?:\s*Memory|\s*Memória)', texto_puro, re.IGNORECASE)
    m_gpu = re.search(r'(?:Graphics|Placa de v[íi]deo):\s*(.*?)(?:\s*DirectX|\s*Storage|\s*Armazenamento|\s*Network)', texto_puro, re.IGNORECASE)
    
    t_cpu = re.split(r'\s+or\s+|\s+ou\s+|/', m_cpu.group(1) if m_cpu else "i5", flags=re.IGNORECASE)[0]
    t_gpu = re.split(r'\s+or\s+|\s+ou\s+|/', m_gpu.group(1) if m_gpu else "GTX 1060", flags=re.IGNORECASE)[0]
    
    t_cpu = re.sub(r'\(.*?\)', '', t_cpu).strip()
    t_gpu = re.sub(r'\(.*?\)', '', t_gpu).strip()

    r_cpu = re.search(r'(i[3579]|Ryzen|FX-|Core|Pentium|Athlon).*', t_cpu, re.IGNORECASE)
    if r_cpu: t_cpu = r_cpu.group(0)

    r_gpu = re.search(r'(GTX|RTX|RX|Radeon|HD|Vega|Arc).*', t_gpu, re.IGNORECASE)
    if r_gpu: t_gpu = r_gpu.group(0)
    
    return t_cpu, t_gpu

def buscar_jogos_por_nome(nome):
    if len(nome) < 3: return []
    url = f"https://store.steampowered.com/api/storesearch/?term={nome}&l=portuguese&cc=BR"
    try:
        res = requests.get(url).json()
        if res.get('items'):
            return [{"label": item['name'], "value": str(item['id'])} for item in res['items']]
    except:
        return []
    return []