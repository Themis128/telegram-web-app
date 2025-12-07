// Service Worker for Telegram Web App PWA
// Version is updated automatically - change this to force cache update
const VERSION = '2025.12.07.2346';
const CACHE_NAME = `telegram-web-app-v${VERSION}`;
const RUNTIME_CACHE = `telegram-runtime-v${VERSION}`;

// Assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing version', VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching static assets');
        // Use cache.addAll with error handling - don't fail if some assets can't be cached
        return Promise.allSettled(
          STATIC_ASSETS.map(url => {
            // Only cache same-origin URLs
            try {
              const urlObj = new URL(url, self.location.origin);
              if (urlObj.protocol === 'chrome-extension:' ||
                  urlObj.protocol === 'chrome:' ||
                  urlObj.protocol === 'moz-extension:' ||
                  urlObj.protocol === 'safari-extension:') {
                console.warn(`Skipping unsupported URL scheme: ${url}`);
                return Promise.resolve();
              }
              return cache.add(url).catch(err => {
                console.warn(`Failed to cache ${url}:`, err);
                // Don't throw - continue with other assets
              });
            } catch (err) {
              console.warn(`Invalid URL ${url}:`, err);
              return Promise.resolve();
            }
          })
        );
      })
      .then(() => {
        // Force activation of new service worker
        return self.skipWaiting();
      })
      .catch((err) => {
        console.error('Service Worker install error:', err);
        // Still activate even if caching fails
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating version', VERSION);
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Delete all caches that don't match current version
          if (!cacheName.includes(`v${VERSION}`)) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      // Take control of all clients immediately
      return self.clients.claim();
    }).then(() => {
      // Notify all clients about the update
      return self.clients.matchAll().then(clients => {
        clients.forEach(client => {
          client.postMessage({
            type: 'SW_UPDATED',
            version: VERSION
          });
        });
      });
    })
  );
});

// Fetch event - network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip unsupported URL schemes
  if (url.protocol === 'chrome-extension:' ||
      url.protocol === 'chrome:' ||
      url.protocol === 'moz-extension:' ||
      url.protocol === 'safari-extension:') {
    return;
  }

  // Skip WebSocket connections
  if (url.protocol === 'ws:' || url.protocol === 'wss:') {
    return;
  }

  // Skip data URLs and blob URLs
  if (url.protocol === 'data:' || url.protocol === 'blob:') {
    return;
  }

  // API calls - network first, cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Only cache successful responses from same origin
          if (response.status === 200 && response.type === 'basic') {
            // Clone the response for caching
            const responseClone = response.clone();

            // Cache in background, don't wait for it
            caches.open(RUNTIME_CACHE).then((cache) => {
              try {
                cache.put(request, responseClone).catch(err => {
                  console.warn('Failed to cache API response:', err);
                });
              } catch (err) {
                console.warn('Error caching API response:', err);
              }
            }).catch(err => {
              console.warn('Failed to open cache for API response:', err);
            });
          }

          return response;
        })
        .catch(() => {
          // Fallback to cache if network fails
          return caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Return offline page or error response
            return new Response(
              JSON.stringify({
                error: 'Offline',
                message: 'You are offline. Please check your connection.'
              }),
              {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
              }
            );
          });
        })
    );
    return;
  }

  // Static assets - network first for HTML, cache first for others
  // This ensures HTML updates are always fresh
  if (url.pathname === '/' || url.pathname === '/index.html') {
    // For HTML files, always fetch from network first, then cache
    event.respondWith(
      fetch(request, { cache: 'no-store' })
        .then((response) => {
          // Only cache if response is valid and from same origin
          if (response && response.status === 200 && response.type === 'basic') {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              try {
                cache.put(request, responseToCache).catch(err => {
                  console.warn('Failed to cache HTML:', err);
                });
              } catch (err) {
                console.warn('Error caching HTML:', err);
              }
            }).catch(err => {
              console.warn('Failed to open cache for HTML:', err);
            });
          }
          return response;
        })
        .catch(() => {
          // Fallback to cache if network fails
          return caches.match(request);
        })
    );
    return;
  }

  // Other static assets - cache first, network fallback
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(request).then((response) => {
          // Don't cache if not a valid response or not from same origin
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response for caching
          const responseToCache = response.clone();

          // Cache in background, don't wait for it
          caches.open(CACHE_NAME).then((cache) => {
            try {
              cache.put(request, responseToCache).catch(err => {
                console.warn('Failed to cache static asset:', err);
              });
            } catch (err) {
              console.warn('Error caching static asset:', err);
            }
          }).catch(err => {
            console.warn('Failed to open cache for static asset:', err);
          });

          return response;
        });
      })
  );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-messages') {
    event.waitUntil(syncMessages());
  }
});

async function syncMessages() {
  // Implement message sync logic here
  console.log('Syncing messages...');
}

// Push notifications (for future use)
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'Telegram';
  const options = {
    body: data.body || 'You have a new message',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    vibrate: [200, 100, 200],
    data: data
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  event.waitUntil(
    clients.openWindow('/')
  );
});
