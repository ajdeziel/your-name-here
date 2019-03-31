/*
* leafletMap.js
*
* For creating and loading OpenStreetMap map with layer created from grave plots data within Ross Bay Cemetery.
* Provide all map interactivity (i.e. popups, event handlers).
*
*/


// Initialize Vue instance with Leaflet.js/Mapbox/OpenStreetMap
// Load grave plots coordinates as map layer on top of embedded OSM map from Mapbox
let plotsLayer = new Vue({
    el: '#map',
    data: {
        map: null,
        tileLayer: null,
        layers: [
            {
                id: 0,
                name: 'Grave Plots',
                active: true,
                features: [

                ],
            }
        ],
    },
    created() {
        fetch("/graves").then(this.populateFeatures);
    },
    mounted() {
        this.initMap();
        // this.initLayers();
    },
    methods: {
        initMap() {
            this.map = L.map('map').setView([48.4107174,-123.3423201], 16)

            this.tileLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYWpkZXppZWwiLCJhIjoiY2p0OWx0bmRrMDFsNjQ5bnV2ZnpyNzJrMCJ9.SSwUPVKs_-Y4vJHmPpBPHA', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.satellite',
                accessToken: 'your.mapbox.access.token'
            })

            this.tileLayer.addTo(this.map);
        },
        // initLayers() {
        //     this.layers.forEach((layer) => {
        //        const circleGraveFeatures = layer.features.filter(feature => feature.type === 'circleMarker');
        //
        //        circleGraveFeatures.forEach((feature) => {
        //            // feature.leafletObject = L.circleMarker(feature.coords).bindPopup(feature.name);
        //            feature.leafletObject = L.Marker([48.4107174,-123.3423201]);
        //
        //        });
        //     });
        // },
        populateFeatures(response) {
            if (response.code !== 200)
                console.log("Failed to get grave information!")
                console.log(response)

            let vue = this;

            response.json().then(function(data) {
                console.log(data)
                vue.features = data
                console.log("Done loading features data.")

                console.log(vue.features)

                L.marker([vue.features[0].latitude, vue.features[0].longitude], L.Icon.Default).addTo(vue.map)
                // vue.initLayers();
                // vue.features.forEach((obj) => {
                //     let x = obj.longitude
                //     let y = obj.latitude
                //
                //     L.marker([y, x], L.Icon.Default).addTo(vue.map)
                // })
            })
        }
    },
});