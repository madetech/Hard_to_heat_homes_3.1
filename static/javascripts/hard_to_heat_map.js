const markersDict = {};
let map;

function initMap() {
    const firstProp = mapData.props[0];
    map = L.map("map").setView([firstProp.lat, firstProp.long], 13);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap",
    }).addTo(map);

    fetch("static/data/bristol_usrn_polygons.json")
        .then((response) => response.json())
        .then((data) => {
            L.geoJSON(data, {
                style: function(feature) {
                    switch (feature.properties.average_epc_score) {
                        case 61: 
                            return {
                                color: "#1bb558",
                                weight: 2,
                            }
                        case 70: 
                            return {
                                color: "#fcaa64",
                                weight: 2,
                            }
                        case null: 
                            return {
                                color: "#9b9b9bd0",
                                weight: 2,
                            }
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
        });

    const scoreIcons = {
        1: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
        }),
        2: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
        }),
        3: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
        }),
        4: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
        }),
    };

    const scoreIconsHover = {
        1: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [30, 51],
            iconAnchor: [17, 56],
            popupAnchor: [1, -34],
            shadowSize: [56, 56],
        }),
        2: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [30, 51],
            iconAnchor: [17, 56],
            popupAnchor: [1, -34],
            shadowSize: [56, 56],
        }),
        3: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [30, 51],
            iconAnchor: [17, 56],
            popupAnchor: [1, -34],
            shadowSize: [56, 56],
        }),
        4: L.icon({
            iconUrl:
                "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
            shadowUrl:
                "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [30, 51],
            iconAnchor: [17, 56],
            popupAnchor: [1, -34],
            shadowSize: [56, 56],
        }),
    };

    const markersPositions = [];

    for (const prop of mapData.props) {

        const score = Number.isInteger(prop.score) ? prop.score : null;

        const marker = L.marker([prop.lat, prop.long], {
            icon: score ? scoreIcons[score] : scoreIcons[1],
        }).addTo(map);

        markersDict[prop.uprn] = marker;

        marker.on("mouseover", function () {
            if (score) marker.setIcon(scoreIconsHover[prop.score]);
        });

        marker.on("mouseout", function () {
           if (score) marker.setIcon(scoreIcons[prop.score]);
        });

        marker.on("click", async () => {
            const address = prop.address

            const popupContent = `
            <div class="custom-popup">
                <a href="/${prop.uprn}">
                      ${address} 
                </a>
                ${score !== null ? `<p class="score-box">Hard to Heat Score: ${score}</p>` : ""}
            </div>
            `;
            marker.bindPopup(popupContent).openPopup();
        });

        markersPositions.push([prop.lat, prop.long]);
    }

    if (markersPositions.length > 0) {
        const bounds = L.latLngBounds(markersPositions);
        map.fitBounds(bounds);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});
