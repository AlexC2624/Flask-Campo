let db_instancia = null;

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