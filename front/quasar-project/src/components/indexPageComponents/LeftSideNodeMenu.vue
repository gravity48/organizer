<template>
  <q-card>
    <q-list>
      <q-item
        v-if="node.source !== 'root'"
        clickable
        v-close-popup
        class="row items-center"
        @click="$emit('editNode',node)"
      >
        <q-icon name="edit" class="q-mr-md" />
        Редактировать подразделение
      </q-item>
      <q-item
        clickable
        v-close-popup
        v-if="node.source !== 'group'"
        class="row items-center"
        @click="$emit('addNode',node)"
      >
        <q-icon name="add" class="q-mr-md" />
        Добавить подразделение
      </q-item>
      <q-item
        clickable
        v-close-popup
        class="row items-center"
        @click="$emit('deleteNode', node)"
        v-if="node.source !== 'root'"
      >
        <q-icon name="delete" class="q-mr-md" />
        Удалить подразделение
      </q-item>
      <q-item
        clickable
        v-close-popup
        class="row items-center"
        @click="$emit('addUser', node)"
        v-if="node.source !== 'root'"
      >
        <q-icon name="person" class="q-mr-md" />
        Добавить пользователя
      </q-item>
    </q-list>
  </q-card>
</template>

<script>
import { defineComponent } from "vue";
export default defineComponent({
  name: 'LeftSideNodeMenu',
  emits:['editNode', 'addNode', 'deleteNode', 'addUser'],
  props: {
    node: {
      type: Object,
      default: ()=>({})
    }
  }
})
</script>
