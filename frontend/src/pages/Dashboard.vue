<script setup>
import StatusCard from '../components/StatusCard.vue'

const statuses = [
  ['当前状态', '待连接'],
  ['设备状态', '离线'],
  ['今日提醒', '0 次'],
  ['连续在座', '0 分钟'],
]
</script>

<template>
  <section>
    <h2>实时监测</h2>
    <div class="cards">
      <StatusCard v-for="status in statuses" :key="status[0]" :title="status[0]" :value="status[1]" />
    </div>
  </section>
</template>

<style scoped>.cards { display: flex; flex-wrap: wrap; gap: 12px; }</style>
