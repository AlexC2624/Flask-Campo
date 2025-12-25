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
    // Captura dos elementos
    const talhao = document.getElementById('talhao').value;
    const atividade = document.getElementById('atividade').value;
    const quantidade = document.getElementById('quantidade').value;
    const dataHora = document.getElementById('dataHora').value;
    const observacoes = document.getElementById('observacoes').value;

    // --- VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS ---
    if (!quantidade || !dataHora) {
        exibirStatus("❌ Preencha a Quantidade e a Data!", "status-erro");
        // Efeito visual de erro no input
        document.getElementById('quantidade').style.borderColor = "#dc3545";
        return;
    }

    // Resetar estilo se estiver ok
    document.getElementById('quantidade').style.borderColor = "#ddd";

    // Criar objeto completo para o IndexedDB
    const novoRegistro = {
        info: `Talhão: ${talhao} | Atividade: ${atividade} | Qtd: ${quantidade}`, // Resumo para o log
        detalhes: {
            talhao,
            atividade,
            quantidade,
            dataHora,
            observacoes
        },
        data_criacao: new Date().toISOString()
    };
    
    try {
        await salvarLocalmente(novoRegistro);
        
        // Limpar campos específicos após salvar
        document.getElementById('quantidade').value = "";
        document.getElementById('observacoes').value = "";
        
        exibirStatus("✅ Salvo com sucesso no aparelho!", "status-sucesso");
        await atualizarContador();
        
        // Tenta sincronizar automaticamente se houver rede
        if (navigator.onLine) {
            sincronizar();
        }
    } catch (e) {
        console.error("Erro ao salvar:", e);
        exibirStatus("❌ Erro ao salvar localmente.", "status-erro");
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        await abrirDB();
        atualizarIndicadorRede();
        await atualizarContador();
    } catch(e) { console.log("DB ainda não disponível"); }
});