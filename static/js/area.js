document.addEventListener("DOMContentLoaded", () => {
    const gpsInput = document.getElementById("gps");
    const mapDiv = document.getElementById("map");

    if (mapDiv) {
        // Default koordinatlar (Bakı mərkəzi)
        let defaultCoords = [40.4093, 49.8671];

        if (gpsInput && gpsInput.value) {
            let parts = gpsInput.value.split(",");
            if (parts.length === 2) {
                defaultCoords = [parseFloat(parts[0]), parseFloat(parts[1])];
            }
        }

        const map = L.map("map").setView(defaultCoords, 13);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
        }).addTo(map);

        let marker = L.marker(defaultCoords, {draggable:true}).addTo(map);

        // marker sürüklənəndə input yenilənsin
        marker.on("dragend", function(e) {
            const pos = marker.getLatLng();
            gpsInput.value = `${pos.lat.toFixed(6)}, ${pos.lng.toFixed(6)}`;
        });

        // xəritəyə klikləyərək marker qoymaq
        map.on("click", function(e) {
            marker.setLatLng(e.latlng);
            gpsInput.value = `${e.latlng.lat.toFixed(6)}, ${e.latlng.lng.toFixed(6)}`;
        });
    }
});
