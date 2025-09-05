// document.addEventListener("DOMContentLoaded", () => {
//     const gpsInput = document.getElementById("gps");
//     const mapDiv = document.getElementById("map");

//     if (mapDiv) {
//         // Default koordinatlar (Bakı mərkəzi)
//         let defaultCoords = [40.4093, 49.8671];

//         if (gpsInput && gpsInput.value) {
//             let parts = gpsInput.value.split(",");
//             if (parts.length === 2) {
//                 defaultCoords = [parseFloat(parts[0]), parseFloat(parts[1])];
//             }
//         }

//         const map = L.map("map").setView(defaultCoords, 13);

//         L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//             maxZoom: 19,
//         }).addTo(map);

//         let marker = L.marker(defaultCoords, {draggable:true}).addTo(map);

//         // marker sürüklənəndə input yenilənsin
//         marker.on("dragend", function(e) {
//             const pos = marker.getLatLng();
//             gpsInput.value = `${pos.lat.toFixed(6)}, ${pos.lng.toFixed(6)}`;
//         });

//         // xəritəyə klikləyərək marker qoymaq
//         map.on("click", function(e) {
//             marker.setLatLng(e.latlng);
//             gpsInput.value = `${e.latlng.lat.toFixed(6)}, ${e.latlng.lng.toFixed(6)}`;
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('get-location');
    const gpsInput = document.getElementById('gps');

    if (!btn || !gpsInput) return;

    btn.addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude.toFixed(6);
                    const lon = position.coords.longitude.toFixed(6);
                    gpsInput.value = `${lat}, ${lon}`;
                    alert(`Konum alındı: ${lat}, ${lon}`);
                },
                function(error) {
                    alert('Konum alınamadı: ' + error.message);
                }
            );
        } else {
            alert('Geolocation dəstəklənmir.');
        }
    });
});
