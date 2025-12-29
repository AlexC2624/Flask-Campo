const CACHE_NAME = 'v16-agro-cargnin';
const ASSETS = [
    '/',
    '/coleta',
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