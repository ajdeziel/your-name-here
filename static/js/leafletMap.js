let plotsLatLong = {[48.4107174, -123.3423201],[48.11, -123.3],[48.99, -123.6],[48.75, -124]}

let plotsLayer = new Vue({
    el: '#content',
    data: {
        map: null,
        tileLayer: null,
        layers: [
            {
                id: 0,
                name: 'Grave Plots',
                active: true,
                features: [],
            },
        ],
    },
    mounted() {
        this.initMap();
        this.initLayers();
    },
    methods: {
        initMap() {
            this.map = L.map('map').setView([48.4107174,-123.3423201], 16);

            this.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYWpkZXppZWwiLCJhIjoiY2p0OWx0bmRrMDFsNjQ5bnV2ZnpyNzJrMCJ9.SSwUPVKs_-Y4vJHmPpBPHA', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.satellite',
                accessToken: 'your.mapbox.access.token'
            });

            this.tileLayer.addTo(this.map);
        },
        initLayers() {},
    },
});