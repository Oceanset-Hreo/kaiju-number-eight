<template>
    <div class="last-page" style="text-align: left;">
        <button class="last-page-btn" @click="onArrowClick">
            <embed  src="./public/arrow-left-circle.svg" 
            type="image/svg+xml" style="width: 30px; pointer-events: none;"/>
        </button>
    </div>
    <p style="font-size: 13px; text-align: left;">Please select a monitoring station.</p>
    <div class="stations-btn-container">
        <div v-for="(station, index) in stations" :key="index">
            <button class="stations-btn" @click="onStationItemClicked(station)">
                <div class="station-icon">
                    <embed src="./public/location_on.svg" type="image/svg+xml" style="width: 30px;"/>
                </div>
                <div class="station-info">
                    <p class="station-name">{{ station.site_name }}</p>
                    <p class="station-coordinate">{{ station.geometry.join(",") }}</p> 
                </div>
                <embed src="./public/chevron-right.svg" type="image/svg+xml" class="arrow-icon"/>
            </button>
        </div>
    </div>
</template>

<script setup>

const props = defineProps({
    stations: {
        type: Array,
        required: true,
    },
    setSideStatus: {
        type: Function,
        required: true,
    },
    handleSpecificStationClick: {
        type: Function,
        required: true,
    },
});

const onArrowClick = () => {
    console.log('onArrowClick clicked');
    props.setSideStatus('CROP_SEARCH');
}

const onStationItemClicked = (station) => {
    console.log('station item clicked')
    console.log(station)
    props.handleSpecificStationClick(station.site_id, station.geometry);
}
</script>

<style>

    .last-page {
        text-align: left;
        width: 90%;
    }

    .last-page-btn {
        padding-left: 0%; 
        padding-bottom: 0%; 
        padding-top: 6%;
        border: none;
        outline: none;
        background-color: #FFFFFF;
    }

    .last-page-btn:hover {
        border: none;
        outline: none;
    }

    .station-icon {
        min-width: 50px; 
        text-align: left;
    }

    .station-coordinate {
        font-size: 16px;
        color: #8A8A8A;
        margin: 0;
    }
</style>