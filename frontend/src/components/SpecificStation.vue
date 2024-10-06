
<script setup>
import { ref, defineProps } from 'vue';
import DataCard from './DataCard.vue';
import CropDataCard from './CropDataCard.vue';

const props = defineProps({
    stationData: {
        type: Object,
        required: true,
    },
    setSideStatus: {
        type: Function,
        required: true,
    },
});


const cropImg_mapping = {
    "banana":       "./public/banana.png",
    "cocoa":        "./public/cocoa.png",
    "coffee":       "./public/coffee.png",
    "cotton":       "./public/cotton.png",
    "groundnut":    "./public/groundnut.png",
    "maize":        "./public/maize.png" ,
    "potato":       "./public/potato.png",
    "soybean":      "./public/soybean.png",
    "wetland rice": "./public/wetland_rice.png",
    "sugarcane":    "./public/sugarcane.png",
    "sugarbeet":    "./public/sugarbeet.png",
    "wheat":        "./public/wheat.png",
    "tea":          "./public/tea.png",
}

const getCropImage = (name) => {
    return cropImg_mapping[name];
};

const emit = defineEmits(['showSuggestPopup', 'showCropPopup']);
const stationData = "Station Information"
const showSuggestPopupWithData = () => {
    emit('showSuggestPopup', stationData);
};

const showCropPopupWithData = (crops, cropImgSrc) => {
    const cropData = {
        crops,
        cropImgSrc: cropImgSrc,
        site: props.stationData.site.site_name,
        site_id: props.stationData.site.site_id
    };
    emit('showCropPopup', cropData);
};

const getManagedCrops = (crops) => {
    const cropMap = {};

    for (let crop of crops) {
        if (crop.name in cropMap) {
            cropMap[crop.name].push(crop)
        } else {
            cropMap[crop.name] = [crop]
        }
    }
    console.log("cropMap", cropMap)
    return cropMap;
}

const getTags = (crops) => {
    return crops.map(crop => crop.analyzer_type);
}

const getReason = (crops) => {
    for (let type of ["Statistics", "RuleBased", "AI"]) {
        for (let crop of crops) {
            if (crop.analyzer_type === type) {
                return crop.reason;
            }
        }
    }
}

const nulltoDash = (value) => {
    if (value === null) {
        return "--";
    }
    return value;
}

const onArrowClick = () => {
    console.log('onArrowClick clicked');
    props.setSideStatus('MULTIPLE_STATIONS');
} 
</script>

<template>
    <div class="last-page" style="text-align: left;">
        <button class="last-page-btn" @click="onArrowClick">
            <embed src="./public/arrow-left-circle.svg" 
            type="image/svg+xml" style="width: 30px; pointer-events: none;"/>
        </button>
    </div>
    <div class="station-head" style="text-align: left;">
        <h2 style="font-size: 32px; line-height: 38.73px;
            margin-top: 5%; margin-bottom: 0%; width: 90%;">
            {{props.stationData.site.site_name }}</h2>
        <p style="font-size: 16px; color: #8a8a8a; margin-top: 0%;">{{props.stationData.site.geometry.join(",")}}</p>
    </div>
    <div class="data-container">
        <p style="font-size: 13px;">Temperature and humidity data (avg.)</p>
        <div class="datas">
            <DataCard dataName="Temperature" :dataValue="nulltoDash(props.stationData.site.airtempmonthliesAverageTempC) + ` °C`"/>
            <DataCard dataName="Relative Humidity" :dataValue="nulltoDash(props.stationData.site.humiditymonthliesAverageDewpointC) + ` °C`"/>
            <DataCard dataName="Monthly Rainfall" :dataValue="nulltoDash(props.stationData.site.precipitationmonthliesLiquidAccumulationMm) + ` mm`"/>
        </div>
    </div>
    <div class="data-container">
        <p style="font-size: 13px;">Soil data (avg.)</p>
        <div class="datas">
            <DataCard dataName="Soil saturation" :dataValue="nulltoDash(props.stationData.site.soilmoistureviagravimetricsSaturatedFlag)"/>
            <DataCard dataName="Soil state" :dataValue="nulltoDash(props.stationData.site.soilmoistureforsmapSoilState)"/>
            <DataCard dataName="Density" :dataValue="nulltoDash(props.stationData.site.soilmoistureforsmapSampleBulkDensityGPerMl)"/>
        </div>
        <!-- <p style="font-size: 13px;">Time range: {searchResults[0].}</p> -->
    </div>
    <div class="suggested-container">
        <div style="text-align: left;">
            <p style="font-size: 13px;">Suggested crops to plant</p>
            <p style="font-size: 10px; width: 90%;">Click the card to learn recommendations on how to grow this crop in this region.</p>
            <p class="suggest-text" @click="showSuggestPopupWithData">
                How we give recommendations.
            </p>
        </div>

        <div v-for="(crops, name, index) in getManagedCrops(props.stationData.suggest_crops)" :key="index" class="crop-data-card-container">
            <button class="crop-data-card"
                @click="showCropPopupWithData(crops, getCropImage(name))">
                <CropDataCard
                    :cropName="name"
                    :cropImgSrc="getCropImage(name)"
                    :tags="getTags(crops)"
                    :reason="getReason(crops)"
                />
            </button>
        </div>
    </div>
</template>

<style>
    .data-container {
        width: 90%;
        margin-top: 5%;
        text-align: left;
    }

    .suggest-text {
        text-align: left;
        font-size: 10px;
        color: #0000ff;
        text-decoration: underline;
        cursor: pointer; /* 滑鼠懸停時顯示手型 */
        display: inline-block;
        margin-top: 10px;
    }

    .suggest-text:hover {
        color: #ff0000; /* 滑鼠懸停時文字變色 */
    }

    .datas{
        display: flex;
        justify-content: space-between;
    }

    .crop-data-card-container{
        width: 90%;
        max-height: 300px;
        overflow: auto;
    }

    .crop-data-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        border: 1px solid #000000;
    }
    .suggested-container{
        max-height: 350px;
        overflow: auto;
    }
</style>