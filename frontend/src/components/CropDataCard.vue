<template>
    <div class="crop-img">
        <img :src="cropImgSrc" alt="crop-img" class="cropImg"/>
    </div>
    <div class="crop-data">
        <div class="crop-name">{{cropName}}</div>
        <div class="describe">{{ props.reason }}</div>
        <div class="analyzer-container">
            <div v-for="(tag, index) in props.tags" :key="index" class="analyzer">{{tag}}</div>
        </div>
    </div>
    <embed src="./public/chevron-right.svg" type="image/svg+xml" class="arrow-icon"/>
</template>

<script setup>

    const props = defineProps({
        cropName: {
            type: String,
            required: true
        },
        cropImgSrc: {
            type: String,
            required: true
        },
        tags: {
            type: Array,
            required: true
        },
        reason: {
            type: String,
            required: true
        }
    });

</script>

<style>
    .crop-data-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        /* margin-top: 10px; */
        border: 1px solid #000000;
        
    }

    .crop-img {
        width: 60px;
        height: 60px;
        background-color: #F5F5F5;
        border-radius: 10px;
        margin-right: 2%;
    }

    .crop-data {
        width: 60%;
        /* height: 100%; */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 10px;
        padding-left: 5%;
        /* text-align: left; */
    }

    .crop-name {
        font-size: 14px;
        font-weight: bold;
        text-align: left;
        padding-left: 2%;
    }

    .describe {
        font-size: 12px;
        color: #8A8A8A;
        text-align: left;
        padding-left: 2%;
    }

    .analyzer-container {
        display: flex;
        justify-content: flex-start;
        gap: 5px;
    }

    .analyzer {
        font-size: 12px;
        border-radius: 25px;
        border: 1px solid #000000;
        padding-left: 5px;
        padding-right: 5px;
        color: #8A8A8A;
    }

    .arrow-icon {
        width: 30px;
    }

    .cropImg {
        width: 100%;
        height: 100%;
    }
</style>