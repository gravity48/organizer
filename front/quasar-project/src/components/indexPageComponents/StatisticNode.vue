<template>
  <div class="statistic-node">
    <q-inner-loading :showing="loading" />
    <div class="statistic-node-item">
      <div class="statistic-node-item-header">
        Количество людей в подразделении:
      </div>
      <div class="statistic-node-item-body">
        {{ count }}
      </div>
    </div>
    <div class="statistic-node-item">
      <div class="statistic-node-item-header">
        Средний возраст в подразделении:
      </div>
      <div class="statistic-node-item-body">
        {{ avgYear || "Нет данных" }}
      </div>
    </div>
    <div class="statistic-node-item">
      <div class="statistic-node-item-header">
        Средний стаж работы в подразделении:
      </div>
      <div class="statistic-node-item-body">
        {{ avgExp || "Нет данных" }}
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
export default defineComponent({
  name: "StatisticNode",
  props: {
    count: {
      type: Number,
      default: null,
    },
    avgYear: {
      type: String,
      default: "",
    },
    avgExp: {
      type: String,
      default: "",
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
});
</script>
<style scoped>
.statistic-node {
  padding: 16px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.statistic-node-item {
  padding: 8px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.statistic-node-item-body {
  color: white;
  background-color: var(--q-primary);
  padding: 2px 8px;
  border-radius: 3px;
}
</style>
