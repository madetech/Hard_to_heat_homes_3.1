const markersDict = {}; 

function initMap() {
    const firstProp = mapData.props[0];
    const map = L.map('map').setView([firstProp.lat, firstProp.long], 13);
    
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    const scoreIcons = {
    1: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    }),
    2: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    }),
    3: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    }),
    4: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    })
};

const scoreIconsHover = {
    1: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [30, 51],
        iconAnchor: [17, 56],
        popupAnchor: [1, -34],
        shadowSize: [56, 56]
    }),
        2: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [30, 51],
        iconAnchor: [17, 56],
        popupAnchor: [1, -34],
        shadowSize: [56, 56]
    }),
    3: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [30, 51],
        iconAnchor: [17, 56],
        popupAnchor: [1, -34],
        shadowSize: [56, 56]
    }),
    4: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [30, 51],
        iconAnchor: [17, 56],
        popupAnchor: [1, -34],
        shadowSize: [56, 56]
    })
};


    const markersPositions = [];

    for (const prop of mapData.props) {
        const marker = L.marker([prop.lat, prop.long], {
        icon: scoreIcons[prop.score] || scoreIcons[1] 
    }).addTo(map);


        markersDict[prop.uprn] = marker;

        marker.on('mouseover', function() {
        marker.setIcon(scoreIconsHover[prop.score]);
    });

    marker.on('mouseout', function() {
        marker.setIcon(scoreIcons[prop.score]);
    });

    marker.on('click', async () => {
            const address = await getAddressFromPlacesAPI(prop.uprn, mapData.apiKey);

            const popupContent = `
            <div class="custom-popup">
                <a href="/${prop.uprn}">
                      ${address} 
                </a>
                <p class="score-box"> Hard to Heat Score: ${prop.score}</p>
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

window.onload = initMap;