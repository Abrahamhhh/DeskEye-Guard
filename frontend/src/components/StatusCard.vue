<script setup>
defineProps({ title: String, value: String })
</script>

<template><article><strong>{{ title }}</strong><p>{{ value }}</p></article></template>

<style scoped>article { min-width: 150px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; }</style>
