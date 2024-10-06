<template>
    <div style="width: 100%; height: 100vh; padding: 0%;">
        <div id="map" class="map-container" style="width: 100%; height: 100vh; padding: 0%;"></div>
    </div>
</template>

<script>
import mapboxgl from 'mapbox-gl';

export default {
  name: 'Mapbox',
  props: {
    center: {
      type: Array,
    },
    accessToken: {
      type: String,
    }
  },
  mounted() {
    mapboxgl.accessToken = this.accessToken;

    const map = new mapboxgl.Map({
        style: 'mapbox://styles/mapbox/outdoors-v12',
        center: this.center,
        zoom: 15.5,
        pitch: 45,
        bearing: -17.6,
        container: 'map',
        antialias: true
    });

    window._globalMap = map;
    map.on('style.load', () => {
        // Insert the layer beneath any symbol layer.
        const layers = map.getStyle().layers;
        const labelLayerId = layers.find(
            (layer) => layer.type === 'symbol' && layer.layout['text-field']
        ).id;

        // The 'building' layer in the Mapbox Streets
        // vector tileset contains building height data
        // from OpenStreetMap.

        map.addLayer(
            {
                'id': 'add-3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 15,
                'paint': {
                    'fill-extrusion-color': '#aaa',

                    // Use an 'interpolate' expression to
                    // add a smooth transition effect to
                    // the buildings as the user zooms in.
                    'fill-extrusion-height': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'height']
                    ],
                    'fill-extrusion-base': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'min_height']
                    ],
                    'fill-extrusion-opacity': 0.6
                }
            },
            labelLayerId
        );
    });

    // const marker = new mapboxgl.Marker()
    //   .setLngLat([121.4737, 31.2304]) // 標記經緯度
    //   .addTo(map); // 將標記添加到地圖

    map.addControl(new mapboxgl.NavigationControl()); // 添加地圖控制
  }
}
</script>

<style scoped>
.map-container {
    width: 100%;
    height: 100%; /* 可根據需求調整 */
}
</style>