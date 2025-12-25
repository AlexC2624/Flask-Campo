const CACHE_NAME = 'v5-coletor';
const ASSETS = [
    '/',
    'menu',
    'coleta',
    '/manifest.json',
    '/static/css/style.css',
    '/static/js/db.js',
    '/static/js/app.js'
];

// Instalação e Cache
self.addEventListener('install', (event) => {
    self.skipWaiting(); 
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('SW: Cacheando todos os arquivos novos');
            return cache.addAll(ASSETS);
        })
    );
});

// Limpeza de caches antigos (Importante para atualizar o HTML)
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('SW: Removendo cache antigo:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

// Resposta: Tenta buscar na rede primeiro, se falhar, usa o cache
// Isso é melhor para desenvolvimento (Network First)
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(event.request);
        })
    );
});