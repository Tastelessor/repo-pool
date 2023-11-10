<template>
  <div class="main">
    <Panel class="panel" @parent_callback="handle_child_emit"></Panel>
    <transition name="fade" mode="out-in">
      <div v-if="show_editor" key="info">
        <JsonEditor class="info"></JsonEditor>
      </div>
      <div v-else key="jsonEditor">
        <Info class="info"></Info>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Panel from './views/Panel.vue'
import Info from './views/Info.vue'
import JsonEditor from './components/JsonEditor.vue'
import { ref } from 'vue'

const show_editor = ref(false)
const handle_child_emit = (data: string) => {
  console.log("Recevied emit from Panel", data)
  show_editor.value = !show_editor.value
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
