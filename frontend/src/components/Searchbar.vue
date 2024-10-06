<script setup>
import { ref, toRefs } from 'vue';
import axios from 'axios';

const searchQuery = ref('');
const updateList = ref([]);
const showList = ref(false);


const props = defineProps({
    Mapbox_access_token: String,
    clickedCrop: {
        type: String,
        default: null
    },
    handleListItemClick: Function
});

const emit = defineEmits(['updateResults, cropClicked']);

const UpdateList = async () => {
    const apiUrl = `https://api.mapbox.com/search/geocode/v6/forward?q=${searchQuery.value}&access_token=${props.Mapbox_access_token}`;
    updateList.value = [];
    axios.get(apiUrl)
        .then((response) => {
            response.data.features.forEach(element => {
                updateList.value.push({
                    "coordinates": element.properties.coordinates,
                    "full_address": element.properties.full_address,
                })
            });
            showList.value = true;
        })
        .catch((error) => {
            console.error(error);
        });
};

const handleSearch = async() => {

    if (searchQuery.value.length > 0) {
        showList.value = false;
        emit('cropClicked', "")
        emit('updateResults', {"site":[
            {'site_name': 'Iowa', 'coordinate': [-93.3899, 42.1746]}, 
            // {'site_name': 'Illinois', 'coordinate': [-89.1965, 40.0417]}, 
            // {'full_name': 'Nebraska', 'coordinate': [-99.9018, 41.4925]}, 
            // {'full_name': 'Minnesota', 'coordinate': [-94.3053, 46.2807]}, 
            // {'full_name': 'Indiana', 'coordinate': [-86.2816, 40.5512]}, 
            // {'full_name': 'South Dakota', 'coordinate': [-99.9018, 43.9695]}, 
            // {'full_name': 'Kansas', 'coordinate': [-98.4842, 38.4847]}
        ]});

        // const apiUrl = `https://api.mapbox.com/search/searchbox/v1/suggest?q=${searchQuery.value}&access_token=${props.Mapbox_access_token}`;
        // try {
        //     const response = await axios.get(apiUrl);
        //     const results = response.data.suggestions;
        //     // 將搜尋結果傳遞給父元件
        //     emit('updateResults', results);
        // } catch (error) {
        //     console.error(error);
        // }
  }
};

</script>

<template>
    <div class="searchbar-container">
        <div class="searchbar">
            <input type="text" 
                placeholder="Search any place" 
                @input="UpdateList" 
                @keyup.enter="handleSearch"
                v-model="searchQuery"/>
            <button class='search-btn' @click="handleSearch">
                <embed src="./public/search-30.svg" type="image/svg+xml" style="padding-top: 2%;"/>
            </button>
        </div>
        <ul class="search-results" v-show="showList && updateList.length > 0">
            <li v-for="(result, index) in updateList" :key="result.id" 
                @click="() => {
                    showList=false; 
                    props.handleListItemClick(result);
                }"
                style=" display: flex;">
                <embed src="./public/location_on.svg" type="image/svg+xml" style="width: 30px;"/>
                <div style="margin-left: 10px;">
                    <div style="font-size: 18px;">{{ result.full_address }}</div>
                </div>
            </li>
        </ul>
    </div>
</template>

<style>
.search-container {
    position: relative;
    width: 100%;
    /* background-color: #000000; */
}

.search-bar {
    width: 100vw;
    display: flex;
    /* align-items: center; */
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
    padding-bottom: 0%;
    background-color: #fdfcfcba;
    color: #000000;
}

.search-btn {
    width: 5%;
    height: 20%;
    border: none;
    background: none;
    /* cursor: pointer; */
    padding: 10px;
    padding-top: 15px;
    padding-bottom: 0%;
    /* margin-top: 10px; */
}

input {
    width: 80%;
    border-radius: 25px;
}

input[type="text"] {
    flex-grow: 1;
    border: none;
    outline: none;
    padding: 10px;
    color: #000000;
}

.search-results {
    width: 60%;
    position: absolute;
    top: 100%;
    left: 23%;
    list-style: none;
    margin-top: 30px;
    background-color: #fdfcfcba;
    border: 1px solid #ccc;
    padding: 2%;
}

.search-results li {
    width: 100%;
    padding-top: 5px;
    margin-right: 2%;
    border-top: 1px solid #ccc;
}
</style>