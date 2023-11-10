<template>
  <div class="main">
    <Panel class="panel" @parent_callback="handle_child_emit"></Panel>
    <Info class="info"></Info>
  </div>

</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Info from './views/Info.vue'
import Panel from './views/Panel.vue'
import { ref } from 'vue'

const handle_child_emit = (data: string) => {
  console.log("Recevied emit from Panel", data)
}

</script>


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
