/*
* leafletMap.js
*
* For creating and loading OpenStreetMap map with layer created from grave plots data within Ross Bay Cemetery.
* Provide all map interactivity (i.e. popups, event handlers).
*
*/

// let plotsLatLong = {[48.4107174, -123.3423201], [48.11, -123.3], [48.99, -123.6], [48.75, -124]}

// Get coords on ready state of an element
function ready(fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

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
                active: false,
                features: [],
            },
        ],
    },
    created() {
        fetch("/graves").then(this.populateFeatures);
    },
    mounted() {
        this.initMap();
        this.initLayers();
    },
    methods: {
        initMap() {
            this.map = L.map('map').setView([48.4107174,-123.3423201], 16);

            this.tileLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYWpkZXppZWwiLCJhIjoiY2p0OWx0bmRrMDFsNjQ5bnV2ZnpyNzJrMCJ9.SSwUPVKs_-Y4vJHmPpBPHA', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.satellite',
                accessToken: 'your.mapbox.access.token'
            });

            this.tileLayer.addTo(this.map);
        },
        initLayers() {
            this.layers.forEach((layer) => {
               const polygonGraveFeatures = layer.features.filter(feature => feature.type === 'polygon');

               polygonGraveFeatures.forEach((feature) => {
                   feature.leafletObject = L.polygon(feature.coords).bindPopup(feature.name);
               });
            });
        },
        populateFeatures(response) {
            if (response.code !== 200)
                console.log("Failed to get grave information!")

            response.json().then(function(data) {
                this.features = data;
                console.log("Done loading features data.")
            }).catch(function() {
                console.log("Failed to parse incoming JSON data.")
            })
        }
    },
});