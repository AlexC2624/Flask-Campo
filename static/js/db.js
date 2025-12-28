let db_instancia = null;

function obterIdAparelho() {
    let id = localStorage.getItem('agro_device_id');
    if (!id) {
        // Gera um ID tipo: AGRO-A1B2C-9999
        id = 'CEL-' + Math.random().toString(36).substr(2, 5).toUpperCase() + '-' + Date.now().toString().slice(-4);
        localStorage.setItem('agro_device_id', id);
    }
    return id;
}

async function abrirDB() {
    if (db_instancia) return db_instancia;
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("ColetorDB", 1);
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains("pendentes")) {
                db.createObjectStore("pendentes", { keyPath: "id", autoIncrement: true });
            }
        };
        request.onsuccess = (e) => {
            db_instancia = e.target.result;
            resolve(db_instancia);
        };
        request.onerror = (e) => reject(e.target.error);
    });
}

async function salvarLocalmente(dado) {
    const db = await abrirDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction("pendentes", "readwrite");
        const store = tx.objectStore("pendentes");
        store.add(dado);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject();
    });
}

async function listarPendentes() {
    const db = await abrirDB();
    return new Promise((resolve) => {
        const tx = db.transaction("pendentes", "readonly");
        const request = tx.objectStore("pendentes").getAll();
        request.onsuccess = () => resolve(request.result);
    });
}

async function removerLocal(id) {
    const db = await abrirDB();
    return new Promise((resolve) => {
        const tx = db.transaction("pendentes", "readwrite");
        tx.objectStore("pendentes").delete(id);
        tx.oncomplete = () => resolve();
    });
}