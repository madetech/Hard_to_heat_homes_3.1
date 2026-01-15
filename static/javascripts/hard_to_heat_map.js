let map;

function getColorForScore(score) {
    if (score >= 3.5) return "#dc3545";
    if (score >= 2.5) return "#fd7e14";
    if (score >= 1.5) return "#fcaa64";
    if (score >= 1.0) return "#1bb558";
    
    return "#9b9b9bd0";
}

// Fallback Logic 
function getScoreFromEPC(epc) {
    if (!epc) return 0;
    if (epc < 39) return 4;
    if (epc < 55) return 3;
    if (epc < 69) return 2;
    return 1;
}

function initMap() {
    let startLat = 51.4545;
    let startLong = -2.5879;
    let zoomLevel = 13;

    if (typeof mapData !== 'undefined' && mapData.props && mapData.props.length > 0) {
        const firstProp = mapData.props[0];
        if (firstProp.lat && firstProp.long) {
            startLat = firstProp.lat;
            startLong = firstProp.long;
            zoomLevel = 15;
        }
    }

    map = L.map("map").setView([startLat, startLong], zoomLevel);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap",
    }).addTo(map);

    const scoresByPostcode = {};
    
    if (typeof mapData !== 'undefined' && mapData.props) {
        mapData.props.forEach(prop => {
            if (prop.postcode && prop.score > 0) {
                const postcode = prop.postcode.replace(/\s/g, '').toUpperCase();
                if (!scoresByPostcode[postcode]) {
                    scoresByPostcode[postcode] = [];
                }
                scoresByPostcode[postcode].push(prop.score);
            }
        });
    }

    fetch("static/data/bristol_usrn_polygons.json")
        .then((response) => response.json())
        .then((data) => {
            L.geoJSON(data, {
                style: function(feature) {
                    let finalScore = 0;
                    if (feature.properties.postcode) {
                        
                        const polygonPostcode = feature.properties.postcode.replace(/\s/g, '').toUpperCase();
                        const scores = scoresByPostcode[polygonPostcode];

                        if (scores && scores.length > 0) {
                            const total = scores.reduce((currentTotal, currentAddressHeatScore) => currentTotal + currentAddressHeatScore, 0);
                            finalScore = total / scores.length;
                        }
                    }

                    // Fallback
                    if (finalScore === 0) {
                        const epc = feature.properties.average_epc_score;
                        finalScore = getScoreFromEPC(epc);
                    }

                    return {
                        color: getColorForScore(finalScore),
                        weight: 2,
                        fillOpacity: 0.6
                    };
                }
            }).addTo(map);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});
