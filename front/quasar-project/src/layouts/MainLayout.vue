<template>
  <q-layout view="lHh Lpr lFf">
    <q-header unelevated>
      <q-toolbar>
        <q-toolbar-title> Organizer </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "MainLayout",

  components: {},
});
</script>
