const CACHE_NAME = 'v11-agro-cargnin';
const ASSETS = [
    '/',
    '/menu',
    '/coleta',
    '/relatorios',
    '/ver_dados',
    '/static/css/style.css',
    '/static/js/db.js',
    '/static/js/app.js',
    '/static/logo.png',
    '/manifest.json'
];

self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Não cacheia downloads de Excel ou envios de POST
    if (event.request.method !== 'GET' || event.request.url.includes('/exportar_excel')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            const fetchPromise = fetch(event.request).then((networkResponse) => {
                // Atualiza o cache com a versão nova da rede
                if (networkResponse.ok) {
                    const clone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                }
                return networkResponse;
            });

            // Retorna o cache se houver, ou a rede se não houver cache
            return cachedResponse || fetchPromise;
        }).catch(() => {
            // Se tudo falhar (totalmente offline e sem cache)
            return caches.match('/');
        })
    );
});