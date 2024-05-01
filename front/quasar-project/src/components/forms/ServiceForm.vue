<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="w-sm q-pa-md">
      <q-card-section>
        {{ cardHeaderText }}
      </q-card-section>
      <q-form @submit.prevent="onFormSubmit">
        <q-card-section>
          <q-input
            v-model="formData.title"
            label="Название"
            :rules="[
              (val) => val.length != '' || 'Название не может быть пустым',
            ]"
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            flat
            color="negative"
            @click="hide"
            class="q-mr-md"
            label="Отмена"
          />
          <q-btn
            unelevated
            :label="cardOkButtonLabel"
            color="primary"
            :loading="loading"
            type="submit"
          />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>
<script>
import { defineComponent } from "vue";
import service from "src/services/service";
export default defineComponent({
  name: "ServiceForm",
  emits: ["ok", "hide"],
  props: {
    node: {
      type: Object,
      default: () => ({}),
    },
    isPatch: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    cardHeaderText() {
      return this.isPatch
        ? `Изменить узел ${this.node.title}`
        : `Добавить узел в ${this.node.title}`;
    },
    cardOkButtonLabel() {
      return this.isPatch ? "Изменить" : "Добавить";
    },
  },
  data() {
    return {
      loading: false,
      formData: {
        title: "",
      },
    };
  },
  methods: {
    show() {
      this.$refs.dialog.show();
    },

    hide() {
      this.$refs.dialog.hide();
    },

    onDialogHide() {
      this.$emit("hide");
    },
    onFormSubmit() {
      if (this.isPatch) {
        this.updateRequest()
      } else {
        this.createRequest()
      }
    },
    createRequest() {
      this.loading = true;
      return service.create(this.formData)
      .catch(()=>{
        this.$notify('Не удалось добавить узел')
      })
      .then(({data})=>{
        this.$notify('Узел успешно добавлен', 'positive')
        this.hide();
        this.$emit('ok', data)
      })
      .finally(()=>{
        this.loading = false
      })
    },
    updateRequest() {
      this.loading = true;
      return service.update(this.pk, this.formData)
        .then(({data})=> {
          this.$notify('Изменено', 'positive')
          this.$emit('ok', data)
          this.hide()
        })
        .catch((e)=>{
          this.$notify('Не удалось изменить узел')
          console.log(e)
        })
        .finally(()=>{
          this.loading = false
        })
    },

    onCancelClick() {
      this.hide();
    },
  },
  created() {
    if (this.isPatch) {
      this.formData.title = this.node.title;
      this.pk = this.node.id
    }
  },
});
</script>
