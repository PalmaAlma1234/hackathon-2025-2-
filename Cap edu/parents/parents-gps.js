// parents-gps.js — запрос геолокации и отправка (POST) на бэкенд эндпоинт /gps
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('getLocation');
  const result = document.getElementById('locResult');

  btn.addEventListener('click', () => {
    result.textContent = 'Запрашиваю местоположение…';
    if (!navigator.geolocation) {
      result.textContent = 'Геолокация не поддерживается в этом браузере.';
      return;
    }

    navigator.geolocation.getCurrentPosition(async (pos) => {
      const coords = {
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude,
        accuracy: pos.coords.accuracy
      };
      result.textContent = `lat: ${coords.latitude.toFixed(5)}, lon: ${coords.longitude.toFixed(5)}`;

      // POST в локальный бэкенд (ФастАПИ) — убедитесь, что бэкенд запущен на localhost:8000
      try {
        const resp = await fetch('http://localhost:8000/gps', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(coords)
        });
        if (resp.ok) {
          const data = await resp.json();
          result.textContent += ' — отправлено на сервер';
        } else {
          result.textContent += ' — ошибка отправки на сервер';
        }
      } catch (err) {
        result.textContent += ' — не удалось соединиться с сервером';
      }

    }, (err) => {
      result.textContent = 'Ошибка получения координат: ' + (err.message || err.code);
    }, { enableHighAccuracy: false, timeout: 10000 });
  });
});
