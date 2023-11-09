<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Info from './views/Info.vue'
import Panel from './views/Panel.vue'
</script>

<template>
  <div class="main">
    <Panel class="panel"></Panel>
    <Info class="info"></Info>
  </div>

</template>

<style scoped>

.main {
  position: absolute;
  display: flex;
  width: 100vw;
  height: 100%;
  left: 0;
  top: 0;
}

.panel {
  position: absolute;
  display: flex;
  width: 30vw !important;
  left: 0;
}

.info {
  position: absolute;
  display: flex;
  width: 70vw !important;
  right: 0;
}

</style>
