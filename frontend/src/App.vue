<script setup>
import { ref } from 'vue'
import Admin from './pages/Admin.vue'
import Dashboard from './pages/Dashboard.vue'
import History from './pages/History.vue'
import Login from './pages/Login.vue'

const currentPage = ref('dashboard')
const pages = { login: Login, dashboard: Dashboard, history: History, admin: Admin }
</script>

<template>
  <main>
    <h1>DeskEye Guard</h1>
    <nav>
      <button @click="currentPage = 'login'">登录页</button>
      <button @click="currentPage = 'dashboard'">实时监测</button>
      <button @click="currentPage = 'history'">历史统计</button>
      <button @click="currentPage = 'admin'">管理员页面</button>
    </nav>
    <component :is="pages[currentPage]" />
  </main>
</template>

<style scoped>
main { max-width: 960px; margin: 0 auto; padding: 24px; font-family: sans-serif; }
nav { display: flex; gap: 8px; margin-bottom: 24px; }
</style>
