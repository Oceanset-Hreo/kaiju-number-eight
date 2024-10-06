<script setup>

import mapboxgl from 'mapbox-gl';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import Mapbox from './components/Mapbox.vue';
import Searchbar from './components/Searchbar.vue';
import InitStationsDetail from './components/InitStationsDetail.vue';
import MultipleStations from './components/MultipleStations.vue';
import EmptyStation from './components/EmptyStation.vue';
import SpecificStation from './components/SpecificStation.vue';
import SuggestPop from './components/SuggestPop.vue';
import CropDataPop from './components/CropDataPop.vue';

const mapboxAccessToken = import.meta.env.VITE_MAPBOXGL_ACCESS_TOKEN;
const baseURL = import.meta.env.VITE_BASE_URL;

const SIDE_STATUS_MAP = {
  CROP_SEARCH: "CROP_SEARCH",
  MULTIPLE_STATIONS: "MULTIPLE_STATIONS",
  NO_RESULT: "NO_RESULT",
  SPEICIFIC_STATION: "SPEICIFIC_STATION"
}

const clickedCrop = ref(null);
const sideStatus = ref(SIDE_STATUS_MAP.NO_RESULT);
const searchResults = ref([]);
const stations = ref([]);
const location = ref("");
const center = ref([121.519486, 25.076386]);
const crops = ref([]);

const updateSearchResults = (results) => {
  console.log(results);
  searchResults.value = results.site;
};

const handleCropTagClick = (crop) => {
  if (crop === clickedCrop.value) {
    clickedCrop.value = null;

  } else {

    clickedCrop.value = crop;
  }

  queryCrops();
};

const setSideStatus = (status) => {
  console.log("setSideStatus", status);
  sideStatus.value = status;
};

const setLocation = (loc) => {
  location.value = loc;
};

const showSuggestPopup = ref(false);
const suggestPopupData = ref('');
const showCropPopup = ref(false);
const cropPopupData = ref({});
const stationData = ref({});

// 用來接收 SpecificStation 傳遞的數據並顯示彈窗
const handleShowSuggestPopup = (data) => {
  suggestPopupData.value = data;
  showSuggestPopup.value = true;
};

// 關閉彈窗
const closeSuggestPopup = () => {
  showSuggestPopup.value = false;
};

const handleShowCropPopup = (data) => {

  axios.get(`${baseURL}/api/advice/${data.site_id}?location=${location.value}`)
    .then((response) => {
      const {suggestion} = response.data;
      console.log(suggestion);

      cropPopupData.value = {
        ...data,
        suggestion
      };
      showCropPopup.value = true;
    })
    .catch((error) => {
      console.error(error);
    });
    
};

const closeCropPopup = () => {
  showCropPopup.value = false;
};

const handleListItemClick = (data) => {
  console.log(JSON.stringify(data));
  location.value = data.full_address;

  const coordinates = data.coordinates;
  const searchResult = axios.get(`${baseURL}/api/list?latitude=${coordinates.latitude}&longitude=${coordinates.longitude}&distance=1000`)
    .then((response) => {
      console.log(response.data);
      if (response.data.length === 0) {
        sideStatus.value = SIDE_STATUS_MAP.NO_RESULT;
        return;
      }
      stations.value = response.data;
      const marker = new mapboxgl.Marker({ className: "water-detail-marker" })

      response.data.forEach((station) => {
        marker.setLngLat(station.geometry)
          .addTo(window._globalMap);
      });
      
      sideStatus.value = SIDE_STATUS_MAP.MULTIPLE_STATIONS;
    })
    .catch((error) => {
      console.error(error);
    });
}

const handleSpecificStationClick = (site_id, geometry) => {
  console.log("handleSpecificStationClick");
  console.log(site_id, geometry);

  window._globalMap.flyTo({
    center: geometry,
    zoom: 15.5,
    pitch: 45,
    bearing: -17.6,
    speed: 1.2,
    curve: 1,
    easing(t) {
      return t;
    }
  });

  const marker = new mapboxgl.Marker({ className: "water-detail-marker" })
    .setLngLat(geometry)
    .addTo(window._globalMap);

  axios.get(`${baseURL}/api/describe/${site_id}?location=${location.value}`)
    .then((response) => {
      console.log("describe data", response.data);
      stationData.value = response.data;
      sideStatus.value = SIDE_STATUS_MAP.SPEICIFIC_STATION;
    })
    .catch((error) => {
      console.error(error);
    });
}

const handleCenterChange = (center) => {
  center.value = center;
};

const handleAdminClick = (crop) => {
  console.log(crop);

  window._globalMap.flyTo({
    center: crop.geometry,
    zoom: 15.5,
    pitch: 45,
    bearing: -17.6,
    speed: 1.2,
    curve: 1,
    easing(t) {
      return t;
    }
  });

};

const queryCrops = () => {
  let url = `${baseURL}/api/search?longitude=${center.value[0]}&latitude=${center.value[1]}&distance=200`;

  if (clickedCrop.value) {
    url += `&crop=${clickedCrop.value}`;
  }

  axios.get(url)
    .then((response) => {
      console.log(response.data);
      crops.value = response.data;
      setSideStatus(SIDE_STATUS_MAP.CROP_SEARCH);
    })
    .catch((error) => {
      console.error(error);
    });
}

onMounted(() => {
  handleListItemClick({
    "coordinates":{"longitude":121.539528,"latitude":25.044743},"full_address":"臺北市, Taipei, Taiwan"
  })
});

</script>

<template id="app">
  <div id="container">
    <div class="searchbar">
      <Searchbar 
        :Mapbox_access_token="mapboxAccessToken"
        @updateResults="updateSearchResults"
        :clickedCrop="clickedCrop" 
        @cropClicked="handleCropClick"
        :handleListItemClick="handleListItemClick"
      />
    </div>
    <div class="mapbox">
      <Mapbox
        :searchResults="searchResults"
        :accessToken="mapboxAccessToken"
        :center="center"
      />
    </div>
    <div class="stations-detail">
      <div class="stations-detail-container">
        
        <template v-if="sideStatus == SIDE_STATUS_MAP.CROP_SEARCH">
          <InitStationsDetail 
            :crops="crops"
            :clickedCrop="clickedCrop" 
            :handleAdminClick="handleAdminClick"
            @cropTagClicked="handleCropTagClick"
          />
        </template>
        <template v-else-if="sideStatus == SIDE_STATUS_MAP.MULTIPLE_STATIONS">
          <MultipleStations
            :stations="stations"
            :setSideStatus="setSideStatus"
            :handleSpecificStationClick="handleSpecificStationClick"
          />
        </template>
        <template v-else-if="sideStatus == SIDE_STATUS_MAP.NO_RESULT">
          <EmptyStation/>
        </template>
        <template v-else-if="sideStatus == SIDE_STATUS_MAP.SPEICIFIC_STATION">
          <SpecificStation 
            :stationData="stationData"
            :setSideStatus="setSideStatus"
            @showSuggestPopup="handleShowSuggestPopup"
            @showCropPopup="handleShowCropPopup"/>
        </template>
      </div>
    </div>

    <div v-if="showSuggestPopup" class="popup-overlay">
      <div class="popup-content">
        <SuggestPop />
        <button class="close" @click="closeSuggestPopup">Close</button>
      </div>
    </div>

    <div v-if="showCropPopup" class="popup-overlay">
      <div class="popup-content">
        <CropDataPop 
        :cropPopupData="cropPopupData"/>
        <button class="close" @click="closeCropPopup">OK</button>
      </div>
    </div>

  </div>
</template>

<style>
  .searchbar {
      z-index: 20;
      width: 80%;
      margin: 0 auto;
      position: absolute;
      top: 5%;
      left: 17%;
      /* transform:s translate(-30%, -50%); */
  }

  .mapbox {
      width: 100vw;
      height: 100vh;
      z-index: 10;
      position: relative;
  }

  .stations-detail {
      z-index: 20;
      width: 400px;
      margin: 0 auto;
      position: absolute;
      top: 5%;
      left: 2%;
      background-color: #FFFFFF;
      padding-left: 2%;
  }

  #container {
      width: 100%;
      height: 100vh;
      margin: auto;
  }
  
  .popup-overlay {
    z-index: 50;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

.popup-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 55%;
}

.close{
  width: 90%;
  background-color: #000000;
  color: #FFFFFF;
  margin-top: 5%;
}

</style>