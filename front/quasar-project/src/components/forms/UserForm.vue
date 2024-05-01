<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="w-xl q-pa-md">
      <q-card-section>
        <div class="text-h6">{{ cardHeaderText }}</div>
      </q-card-section>
      <q-form @submit.prevent="submitForm">
        <q-card-section>
          <q-input v-model="unitTitle" label="Подразделение" clearable readonly>
            <template #append>
              <q-icon name="apartment" />
            </template>
          </q-input>
          <q-input
            v-model="formData.post"
            clearable
            label="Должность"
            :rules="[required]"
          >
            <template #append>
              <q-icon name="person" />
            </template>
          </q-input>
          <q-input
            v-model="formData.full_name"
            label="ФИО"
            clearable
            :rules="[required]"
          >
            <template #append>
              <q-icon name="person" />
            </template>
          </q-input>
          <q-input
            v-model="formData.birthday"
            label="Дата рождения"
            :rules="[required]"
            clearable
            mask="##.##.####"
          >
            <template #append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date v-model="formData.birthday" mask="DD.MM.YYYY">
                    <div class="row items-center justify-end">
                      <q-btn
                        v-close-popup
                        label="закрыть"
                        color="primary"
                        flat
                      />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-file
            v-model="formData.photo"
            accept="image/*"
            label="Выберите фото"
            clearable
          >
            <template #append>
              <q-icon name="attach_file" />
            </template>
          </q-file>
          <q-input
            v-model="formData.start_at"
            label="Дата поступления на работу"
            :rules="[required]"
            clearable
            mask="##.##.####"
          >
            <template #append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date v-model="formData.start_at" mask="DD.MM.YYYY">
                    <div class="row items-center justify-end">
                      <q-btn
                        v-close-popup
                        label="закрыть"
                        color="primary"
                        flat
                      />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
          <q-img ref="img" :src="imgSrc" />
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
import { required } from "src/utils/formUtils";
import employee from "src/services/employee";

export default defineComponent({
  name: "ServiceForm",
  emits: ["ok", "hide"],
  props: {
    user: {
      type: Object,
      default: () => ({}),
    },
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
        ? `Изменить ${this.user?.full_name}`
        : "Добавить нового пользователя";
    },
    cardOkButtonLabel() {
      return this.isPatch ? `Изменить` : "Добавить";
    },
    required() {
      return required;
    },
    imgSrc() {
      if (!this.formData.photo) return "";
      if (typeof this.formData.photo === "string") {
        return this.formData.photo;
      }
      return URL.createObjectURL(this.formData.photo);
    },
  },
  data() {
    return {
      loading: false,
      formData: {
        full_name: "",
        birthday: null,
        photo: null,
        division_id: null,
        start_at: null,
        post: "",
      },
      unitTitle: "",
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
    onCancelClick() {
      this.hide();
    },
    initializeUpdateFormData() {
      const output = {};
      Object.keys(this.formData).forEach((key) => {
          if (key === "photo" && typeof this.formData[key] === "string") {
          } else {
            output[key] = this.formData[key];
          }
      })
      return output
    },
    createEmployee() {
      this.loading = true;
      return employee
        .create(this.formData)
        .catch(() => {
          this.$notify("Не удалось добавить сотрудника");
        })
        .then(() => {
          this.$notify("Добавлен сотрудник", "positive");
          this.$emit("ok");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateEmployee() {
      this.loading = true;
      return employee
        .update(this.user.id, this.initializeUpdateFormData())
        .then(({ data }) => {
          this.$notify("Обновлено", "positive");
          this.$emit("ok", data);
        })
        .catch((e) => {
          console.log(e)
          this.$notify("Не удалось обновить сотрудника", "negative");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    submitForm() {
      if (this.isPatch) {
        this.updateEmployee();
      } else {
        this.createEmployee();
      }
    },
  },
  created() {
    if (this.isPatch) {
      this.formData.division_id = this.user.division_id;
      this.formData.birthday = this.user.birthday;
      this.formData.full_name = this.user.full_name;
      this.formData.photo = this.user.photo;
      this.formData.post = this.user.post;
      this.formData.start_at = this.user.start_at;
      this.unitTitle = this.user.division_title;
    } else {
      this.unitTitle = this.node.title;
      this.formData.division_id = this.node.division_id;
    }
  },
});
</script>
