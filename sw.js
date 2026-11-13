const CACHE_NAME = 'hamza-traders-v3';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.add('./'))
  );
  self.skipWaiting();
});



self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache =>
            cache.put(event.request, copy)
          );
        }
        return response;
      })
      .catch(() => caches.match(event.request).then(
        cached => cached || caches.match('./')
      ))
  );
});
