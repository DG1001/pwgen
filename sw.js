const CACHE_NAME = 'password-generator-v4';

// Relative to the service worker's own URL, so the app also works when it is
// served from a sub-path (e.g. https://user.github.io/pwgen/).
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/app.css',
  './assets/fonts/inter-latin.woff2',
  './words/en.txt',
  './words/de.txt',
  './words/sentence-en.json',
  './words/sentence-de.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// The page sends this once the user accepts the update prompt. Without it the
// new worker would stay in 'waiting' until every tab is closed.
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', (event) => {
  const request = event.request;

  if (request.method !== 'GET') return;
  if (new URL(request.url).origin !== self.location.origin) return;

  // Navigations: network first, so a new deployment is picked up as soon as
  // the device is online instead of being pinned to the cached shell.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put('./index.html', copy));
          return response;
        })
        .catch(() => caches.match('./index.html').then(
          (cached) => cached || new Response('Offline', { status: 503 })
        ))
    );
    return;
  }

  // Static assets: cache first.
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (response.ok && response.type === 'basic') {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        }
        return response;
      }).catch(() => new Response('Offline', { status: 503 }));
    })
  );
});
