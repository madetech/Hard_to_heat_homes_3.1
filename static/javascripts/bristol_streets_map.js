let map;
let streetLayer;

function initMap() {
    map = L.map('leaflet-container').setView([51.463907, -2.584353], 17)

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    fetch('/static/data/bristol_streets_grouped.geojson')
        .then(response => response.json())
        .then(data => {
            streetLayer = L.geoJSON(data, {
                style: function (feature) {
                    const epc_score = Number(feature.properties.epc_score);
                    if (isNaN(epc_score))
                        return {
                            color: "#c1c1c1ff",
                            weight: 2,
                        };

                    if (epc_score >= 80) {
                        return {
                            color: "#00ff95ff",
                            weight: 2,
                        };
                    }
                    if (epc_score >= 60) {
                        return {
                            color: "#d4ff00ff",
                            weight: 2,
                        };
                    }
                    if (epc_score >= 40) {
                        return {
                            color: "#ffbb00ff",
                            weight: 2,
                        };
                    }
                    if (epc_score < 40) {
                        return {
                            color: "#ff0000ff",
                            weight: 2,
                        };
                    }
                },

                onEachFeature: function (feature, layer) {
                    epc_score = feature.properties.average_epc_score
                        ? feature.properties.average_epc_score
                        : "unknown";
                    layer.bindPopup(
                        "Number of buildings: 30" +
                            "<br>" +
                        "Address: " +
                            feature.properties.address +
                            "<br>" +
                        "Postcode: " +
                            feature.properties.postcode +
                            "<br>" +
                        "Average EPC Score: " +
                            epc_score
                    );
                },
            }).addTo(map);
        })
        .catch(() => console.error("Something went wrong!"));
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});