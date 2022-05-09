// https://chodounsky.com/2019/03/24/progressive-web-application-as-a-share-option-in-android/
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js', { scope: '/' })
    .then(() => { })
    .catch((_err) => { });
}
self.addEventListener('fetch', function (event) { });
