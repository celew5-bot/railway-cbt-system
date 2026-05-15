const CACHE_NAME = 'railway-cbt-v1';

// We cache the core structure immediately when the app is installed
const CORE_ASSETS = [
    '/',
    '/candidate/login',
    '/manifest.json'
];

// 1. Install Event - Cache Core Assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('Opened cache');
            return cache.addAll(CORE_ASSETS);
        })
    );
    self.skipWaiting();
});

// 2. Activate Event - Clean up old caches if we update the app
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// 3. Fetch Event - Network First, falling back to Cache
self.addEventListener('fetch', event => {
    // DO NOT cache the API calls (we will handle offline scores with IndexedDB later)
    if (event.request.url.includes('/api/save_test_result')) {
        return; 
    }

    event.respondWith(
        fetch(event.request)
            .then(response => {
                // If the network works, save a copy to the cache for later
                if (response && response.status === 200 && response.type === 'basic') {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return response;
            })
            .catch(() => {
                // IF THE NETWORK FAILS (OFFLINE), pull the file from the cache!
                return caches.match(event.request);
            })
    );
});