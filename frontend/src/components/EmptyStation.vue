<template>
    <div class="last-page" style="text-align: left;">
        <button class="last-page-btn">
            <embed src="./public/arrow-left-circle.svg" 
            type="image/svg+xml" style="width: 30px; pointer-events: none;"/>
        </button>
    </div>
    <div class="empty-icon">
        <embed src="./public/empty.svg" type="image/svg+xml" style="width: 50%;"/>
    </div>
    <h3>No Results</h3>
    <p style="color: #8A8A8A;">Please try searching again.</p>
</template>

<script setup>
</script>

<style>
    .empty-icon {
        width: 100%;
        text-align: center;
        padding-top: 70%;
    }
</style>