<template>
    <div class="suggest-content">
        <div class="crop-pop-head">
            <div class="crop-pop-img">
                <img :src="cropPopupData.cropImgSrc" alt="crop-img" class="cropImg"/>
            </div>
            <div class="crop-pop-title">
                <h2>How to grow {{cropPopupData.crops[0].name}} in {{cropPopupData.site }}</h2>
            </div>
        </div>
        <div class="crop-pop-content">
            <div class="ai-analyzer">
                <h2>AI Data Insights</h2>
                {{ cropPopupData.suggestion }}
            </div>

            <div v-if="getCrop('AI')" class="analyzers">
                <h2>Suggestion based on agriculturl data</h2>
                {{ getCrop('AI').reason }}
            </div>

            <div v-if="getCrop('RuleBased')" class="analyzers">
                <h2>Suggestion based on data analysis</h2>
                {{ getCrop('RuleBased').reason }}
            </div>


            <div v-if="getCrop('Statistics')" class="analyzers">
                <h2>Planting Suggestions for the Region</h2>
                {{ getCrop('Statistics').reason }}
            </div>
        </div>  
    </div>
</template>

<script setup>
    import { ref, defineProps, onMounted } from 'vue';

    const props = defineProps({
        cropPopupData: {
            type: Object,
            required: true
        },
    });

    onMounted(() => {
        console.log(props.cropPopupData);
        console.log(JSON.stringify(props.cropPopupData));
    });

    const getCrop = (type) => {
        const crops = props.cropPopupData.crops;
        let ruleBasedCrop;

        for (let crop of crops){
            if (crop.analyzer_type === type){
                return crop;   
            }
        }

        return null;
    }

</script>

<style>
    .crop-pop-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 95%;
        height: 10%;
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
    }

    .crop-pop-title {
        width: 80%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 10px;
    }

    .ai-analyzer{
        width: 95%;
        background-color: #F2F2F7;
        padding: auto;
        margin-bottom: 10px;
        padding: 2%;
    }

    .analyzers {
        width: 95%;
        padding: auto;
        margin-bottom: 10px;
        padding: 2%;
    }

    .analyzer-title{
        font-size: 15px;
        font-weight: bold;
    }

    .analyzer-content{
        font-size: 13px;
    }

</style>