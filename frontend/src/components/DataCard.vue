<template>
    <div class="data-card">
        <div id="myChart">
            <div class="data-name">{{ dataName }}</div>
            <div class="data-value">{{ dataValue }}</div>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        dataName: {
            type: String,
            required: true,
        },
        dataValue: {
            type: String,
            required: true,
        },
    });

</script>

<style>
    .data-card{
        width: 28%;
        height: 80px;
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 5px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .data-name{
        height: 40px;
        font-size: 14px;
        color: #8a8a8a;
        text-align: center;
    }

    .data-value{
        font-size: 18px;
        color: #000000;
    }

</style>