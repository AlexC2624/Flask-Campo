// Funções de Interface
function atualizarIndicadorRede() {
    const badge = document.getElementById('status-conexao');
    if (!badge) return;
    badge.className = navigator.onLine ? "badge online" : "badge offline";
    badge.innerHTML = navigator.onLine ? '<i class="fas fa-circle"></i> Online' : '<i class="fas fa-circle"></i> Offline';
}

async function atualizarContador() {
    const itens = await listarPendentes();
    // Tenta encontrar pelo ID direto ou pelo seletor antigo para evitar erros
    const contadorEl = document.getElementById('cont-num') || document.querySelector('#contador strong');
    const btnSync = document.querySelector('.btn-sync');

    if (contadorEl) {
        contadorEl.innerText = itens.length;
    }

    // Lógica visual do botão de sincronização
    if (btnSync) {
        if (itens.length === 0) {
            btnSync.classList.add('sincronizado');
            btnSync.innerHTML = '<i class="fas fa-check-circle"></i> Sincronizado';
            btnSync.style.opacity = "0.6";
        } else {
            btnSync.classList.remove('sincronizado');
            btnSync.innerHTML = '<i class="fas fa-sync-alt"></i> Sincronizar Agora';
            btnSync.style.opacity = "1";
        }
    }
}

async function sincronizar() {
    if (!navigator.onLine) {
        atualizarIndicadorRede();
        return;
    }

    const itens = await listarPendentes();
    if (itens.length === 0) return;

    atualizarIndicadorRede();
    exibirStatus(`Sincronizando ${itens.length} registros...`, "status-online");

    for (const item of itens) {
        try {
            const res = await fetch('/salvar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Enviamos o objeto completo 'detalhes' para o Python
                body: JSON.stringify(item.detalhes) 
            });
            
            if (res.ok) {
                await removerLocal(item.id);
                await atualizarContador();
            }
        } catch (e) {
            console.log("Conexão instável...");
            break; 
        }
    }
}

async function salvarEntrada() {
    const talhao = document.getElementById('talhao').value;
    const atividade = document.getElementById('atividade').value;
    const quantidade = document.getElementById('quantidade').value;
    const dataHora = document.getElementById('dataHora').value;

    const novoRegistro = {
        detalhes: {
            aparelho: obterIdAparelho(), // Identificador automático
            talhao,
            atividade,
            quantidade,
            dataHora
        }
    };
    
    try {
        await salvarLocalmente(novoRegistro);
        exibirStatus(`✅ Salvo! (ID: ${obterIdAparelho()})`, "status-sucesso");
        await atualizarContador();
        if (navigator.onLine) sincronizar();
    } catch (e) {
        exibirStatus("❌ Erro ao salvar", "status-erro");
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        await abrirDB();
        atualizarIndicadorRede();
        await atualizarContador();
    } catch(e) { console.log("DB ainda não disponível"); }
});