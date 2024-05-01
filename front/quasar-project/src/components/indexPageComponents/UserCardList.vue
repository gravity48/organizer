<template>
  <div class="row q-ma-md overflow-auto" style="align-content: flex-start">
    <q-inner-loading :showing="loading" />
    <user-card
      v-for="user in users"
      :key="user.id"
      :user="user"
      class="q-ma-md"
      @update-user="userUpdate"
      @delete-user="userDelete"
    />
  </div>
</template>

<script>
import UserCard from "./UserCard.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "UserCardList",
  emits: ["deleteUser", "updateUser"],
  components: {
    UserCard,
  },
  props: {
    users: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    userUpdate(user) {
      this.$emit("updateUser", user);
    },
    userDelete(user) {
      this.$emit("deleteUser", user);
    },
  },
});
</script>

<style scoped>
.user-list {
  display: flex;
}
</style>
