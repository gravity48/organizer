<template>
  <div class="row justify-between items-center" style="height: 36px">
    <span class="card-fio">
      {{ fio }}
      <q-tooltip>
        {{ fio }}
      </q-tooltip>
    </span>
    <div class="row">
      <q-btn
        flat
        icon="delete"
        color="negative"
        class="q-mr-sm"
        @click="$emit('deleteUser', user)"
      />
      <q-btn flat icon="edit" @click="$emit('updateUser', user)" />
    </div>
  </div>
</template>
<script>
import { defineComponent } from "vue";
export default defineComponent({
  name: "UserCardFooter",
  emits: ["deleteUser", "updateUser"],
  props: {
    fio: {
      type: String,
      default: "",
    },
  },
});
</script>
<style scoped>
.card-fio {
  font-size: 18px;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
