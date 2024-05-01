<template>
  <div class="user-card">
    <div class="row no-wrap overflow-auto" style="flex: 1">
      <div class="img-wrapper">
        <img class="" :src="user.photo" />
      </div>
      <user-card-body
        :post="user.post"
        :dateBirthday="user.birthday"
        :dateStart="user.start_at"
      />
    </div>
    <user-card-footer
      :fio="user.full_name"
      @delete-user="$emit('deleteUser', user)"
      @update-user="$emit('updateUser', user)"
    />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import UserCardBody from "src/components/indexPageComponents/UserCardBody.vue";
import UserCardFooter from "src/components/indexPageComponents/UserCardFooter.vue";

export default defineComponent({
  name: "UserCard",
  components: {
    UserCardBody,
    UserCardFooter,
  },
  emits: ["deleteUser", "updateUser"],
  props: {
    user: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {};
  },
  computed: {
  },
});
</script>
<style scoped>
.user-card {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
  width: 390px;
  height: 170px;
  background-color: var(--app-grey);
  transition: box-shadow 0.35s ease, transform 0.35s ease;
}
.img-wrapper {
  width: 100px;
  height: 100px;
  overflow: hidden;
  margin-right: 16px;
}

.img-wrapper img {
  width: 100%;
}

.user-card:hover {
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
  transform: translateY(-5px);
}
</style>
