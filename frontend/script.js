let timeoutBusca;

async function carregarDatalists() {
    try {
        const res = await fetch('http://127.0.0.1:8000/listar-pecas');
        const data = await res.json();
        
        const cpuDatalist = document.getElementById('lista-cpus');
        const gpuDatalist = document.getElementById('lista-gpus');

        data.cpus.forEach(nome => {
            let opt = document.createElement('option');
            opt.value = nome;
            cpuDatalist.appendChild(opt);
        });

        data.gpus.forEach(nome => {
            let opt = document.createElement('option');
            opt.value = nome;
            gpuDatalist.appendChild(opt);
        });
    } catch (e) {
        console.error(e);
    }
}

async function pesquisarJogo(valor) {
    if (valor.length < 3) return;

    clearTimeout(timeoutBusca);
    timeoutBusca = setTimeout(async () => {
        try {
            const res = await fetch(`http://127.0.0.1:8000/buscar-jogo-steam?nome=${valor}`);
            const jogos = await res.json();
            
            const datalist = document.getElementById('lista-jogos');
            datalist.innerHTML = "";

            jogos.forEach(jogo => {
                let opt = document.createElement('option');
                opt.value = jogo.label;
                opt.dataset.id = jogo.value;
                datalist.appendChild(opt);
            });
        } catch (e) {
            console.error(e);
        }
    }, 500);
}

document.getElementById('jogo_search').addEventListener('change', function() {
    const opts = document.getElementById('lista-jogos').options;
    for (let i = 0; i < opts.length; i++) {
        if (opts[i].value === this.value) {
            document.getElementById('app_id').value = opts[i].dataset.id;
            break;
        }
    }
});

async function verificar() {
    const resDiv = document.getElementById('result');
    const btn = document.querySelector('button');
    
    resDiv.style.display = "none";
    btn.innerText = "PROCESSANDO...";

    const payload = {
        cpu_usuario: document.getElementById('cpu_user').value,
        gpu_usuario: document.getElementById('gpu_user').value,
        app_id_steam: document.getElementById('app_id').value
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/verificar-jogo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            // Define a cor da caixa com base no nível
            if (data.nivel >= 3) {
                resDiv.className = "status-roda";
            } else if (data.nivel === 2) {
                resDiv.className = "status-sofrendo";
            } else {
                resDiv.className = "status-nao-roda";
            }
            
            resDiv.style.display = "block";
            resDiv.innerHTML = `
                <strong style="font-size: 1.2rem">${data.jogo}</strong><br>
                <h2 style="margin: 10px 0">${data.veredicto_final}</h2>
                <div style="text-align: left; font-size: 0.9rem; border-top: 1px solid #333; padding-top: 10px">
                    <b>CPU Steam:</b> ${data.cpu.peca} (${data.cpu.score_exigido})<br>
                    <span style="color: #ccc">➥ O seu PC: ${data.cpu.status}</span><br><br>
                    
                    <b>GPU Steam:</b> ${data.gpu.peca} (${data.gpu.score_exigido})<br>
                    <span style="color: #ccc">➥ O seu PC: ${data.gpu.status}</span>
                </div>
            `;
        } else {
            alert(data.detail);
        }
    } catch (err) {
        alert("Erro de conexão com a API");
    } finally {
        btn.innerText = "ANALISAR SISTEMA";
    }
}

document.addEventListener('DOMContentLoaded', carregarDatalists);