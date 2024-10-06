<template>
    <div class="stations-detail-head">
        <h2 style="font-size: 28px; line-height: 38.73px;
            margin-bottom: 2%; margin-top: 5%; width: 90%;">
            View the top most suitable crops to plant nearby.</h2>
    </div>
    <div class="crops">
        <p class="crops-text" style="font-size: 13px;"> View crop product rankings in </p>
        <div class="crops-list-container">
            <div v-for="(crop, index) in visibleCropTags" :key="index">
                <button 
                    :class="{'active-crop': props.clickedCrop === crop}"
                    class="crop-btn"
                    @click="handleCropTagClick(crop)">{{ crop }}</button>
            </div>

            <button v-if="hiddenCropTags.length > 0 && !showAll" @click="showAll = true" class="more-btn">
                {{ hiddenCropTags.length }}+
            </button>

            <div v-if="showAll" v-for="(crop, index) in hiddenCropTags" :key="'hidden' + index">
                <button 
                    :class="{'active-crop': props.clickedCrop === crop}"
                    class="crop-btn"
                    @click="handleCropTagClick(crop)">{{ crop }}</button>
            </div>
        </div>
    </div>
    <div class="line" style="width: 90%; padding-top: 5%;"> 
        <hr>
    </div>
    <div class="stations">
        <p class="stations-text" style="font-size: 13px; text-align: left;"> The Top 10 {{ chooseCrop }} Producing Regions </p>
        <div class="stations-btn-container">
            <div v-for="(crop, index) in crops" :key="index">
                <button class="stations-btn" @click="handleAdminClick(crop)">
                    <div class="index-container">
                        <h2>{{ index+1 }}</h2>
                    </div>
                    <div class="station-info">
                        <p class="station-name">{{ crop.name }}</p>
                    </div>
                    <embed src="./public/chevron-right.svg" type="image/svg+xml" class="arrow-icon"/>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, defineEmits} from 'vue';

const props = defineProps({
    crops: {
        type: Array,
        required: true,
    },
    clickedCrop: {
        type: String,
        default: null
    },
    handleAdminClick: {
        type: Function,
        required: true
    }
});

const cropTags = ref([
    "maize","wheat","soybean","cotton","sugarcane","sugarbeet","groundnut","potato","banana","coffee","tea","cocoa", "wetland rice"
]);

const showAll = ref(false);
const chooseCrop = ref(props.clickedCrop);

const visibleCropTags = computed(() => {
    return cropTags.value.slice(0, 5);
});

const hiddenCropTags = computed(() => {
    return cropTags.value.slice(5);
});

const emit = defineEmits(['cropTagClicked']);
const handleCropTagClick = (crop) => {
    // 發送 crop 被點擊的事件到父元件
    console.log('chooseCrop', chooseCrop);
    chooseCrop.value = crop;
    emit('cropTagClicked', crop);
};

</script>

<style>
    .stations-detail-container {
        position: relative;
        width: 100%;
        height: 88vh;
        padding: 0, 5px;
        margin-right: 2%;
        /* background-color: aquamarine; */
    }

    .stations-detail-head {
        width: 100%;
        text-align: left;
    }

    .crops {
        text-align: left;
    }

    .crops-list-container {
        padding: 0;
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        max-height: 100px; 
        overflow-y: auto;
        margin-right: 2%;
    }

    .crop-btn, .more-btn {
        padding: 5px 10px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.3s ease; 
        background-color: white; 
        color: black; 
        border: 1px solid black;
    }

    .active-crop {
        padding: 5px 10px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.3s ease;
        background-color: black;
        color: white;
        border: 1px solid black;
    }

    .crop-btn:hover, .more-btn:hover {
        background-color: black; 
        color: white; 
        border: none;
        border: 1px solid black; 
    }

    .stations{
        width: 100%;
        height: 55%;
    }

    .stations-btn-container {
        padding: 0;
        gap: 5px;
        max-height: 100%; 
        overflow-y: auto;
    }

    .stations-btn {
        display: flex; 
        align-items: center; 
        width: 90%; 
        padding: 10px;
        background-color: #FFFFFF; 
        border: 1px solid black;
        border-radius: 5px;
        cursor: pointer;
        text-align: left; 
        margin: 5px 0; 
    }

    .index-container {
        min-width: 50px; 
        text-align: left;
    }

    .station-info {
        margin-left: 0px; 
    }

    .station-name {
        font-size: 16px;
        color: #000000;
        margin: 0; 
    }

    .station-value {
        font-size: 12px;
        color: #000000;
        margin: 0;
    }

    .index-container h2 {
        font-size: 30px;
        color: #d7d7d7;
        margin: 0; 
    }

    .arrow-icon {
        margin-left: auto; 
        width: 20px; 
        height: 20px;
    }

</style>