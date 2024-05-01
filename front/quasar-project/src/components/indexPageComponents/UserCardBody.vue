<template>
  <div class="user-card_info">
    <div class="user-card-description">
      <div class="user-card-description-item">Должность: {{ post }}</div>
      <div class="user-card-description-item">
        Дата рождения: {{ dateBirthday }}
      </div>
      <div class="user-card-description-item">
        Дата начала работы в подразделении:
        {{ dateStart }}
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
export default defineComponent({
  name: "UserCardBody",
  props: {
    fio: {
      type: String,
      default: "",
    },
    post: {
      type: String,
      default: "",
    },
    dateBirthday: {
      type: String,
      default: '',
    },
    dateStart: {
      type: String,
      default: '',
    },
  },

});
</script>
<style scoped>
.user-card-fio {
  text-align: center;
  font-weight: 600;
}

.user-card_info {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 250px;
}
</style>
