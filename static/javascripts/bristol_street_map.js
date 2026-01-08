let map;
let streetLayer;

function initMap() {
    // Initialize the Leaflet map
    map = L.map('leaflet-container').setView([51.454, -2.5879], 13) // Center on Bristol

    // Add basic OpenstreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    fetch('/static/data/bristol_streets_grouped.geojson')
        .then(response => response.json())
        .then(data => {
            // Create the street layer
            streetLayer = L.geoJSON(data, {
                style: {
                    color: "orange",
                    weight: 1,
                    fillColor: "yellow",
                    fillOpacity: 0.5
                }
            }).addTo(map);
        })
        .catch(err => console.log("Error loading GeoJSON", err));
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});