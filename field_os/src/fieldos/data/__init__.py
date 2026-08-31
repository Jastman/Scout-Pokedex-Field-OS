"""Data layer. Rule zero (rev 24): EVERY write is atomic - temp file, fsync,
rename - and the Pi is never unplugged while running.

Finds log: GeoJSON + photo thumbnails on the NVMe. Offline CesiumJS tile store
(Natural Earth II base + high-detail home region, downloaded on desk WiFi).
Home-WiFi sync script pushes finds to the public web twin (GitHub Pages +
Cesium ion token that lives ONLY in the web app, never on the device).
"""
