<template>
  <q-card class="left-side">
    <q-card-section>
      <div class="text-h6">Подразделения</div>
    </q-card-section>
    <q-card-section>
      <q-tree
        :nodes="tree"
        node-key="division_id"
        ref="tree"
        v-model:selected="selectedNode"
        @lazy-load="onLazyLoad"
        selected-color="teal"
        @update:selected="updateTreeNode"
      >
        <template #default-header="{ node }">
          <div>{{ node.title }}</div>
          <q-menu context-menu>
            <LeftSideNodeMenu
              :node="node"
              @editNode="editNode"
              @addNode="addNode"
              @deleteNode="confirmDeleteNode"
              @addUser="addUser"
            />
          </q-menu>
        </template>
      </q-tree>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent } from "vue";
import sources from "src/domain/managementStrcut";
import LeftSideNodeMenu from "./LeftSideNodeMenu.vue";
import UserForm from "../forms/UserForm.vue";

export default defineComponent({
  name: "LeftSide",
  emits: [
    "onLazyLoad",
    "updateNode",
    "addNode",
    "deleteNode",
    "update:treeNodeClicked",
    "addUser"
  ],
  components: {
    LeftSideNodeMenu,
  },
  props: {
    tree: {
      type: Array,
      default: () => [],
    },
    treeNodeCLicked: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      selectedNode: "",
    };
  },
  methods: {
    onLazyLoad(params) {
      this.$emit("onLazyLoad", params);
    },
    updateTreeNode(value) {
      const node = this.$refs.tree.getNodeByKey(value);
      this.$emit("update:treeNodeClicked", node);
    },
    editNode(node) {
      const formComponent = sources.getForm(node.source);
      this.$q
        .dialog({
          component: formComponent,
          componentProps: {
            node: node,
            isPatch: true,
          },
        })
        .onOk((data) => {
          this.$emit("updateNode", { ...data, source: node.source });
        });
    },
    addUser(node) {
      const addUserFormDialog = this.$q.dialog({
        component: UserForm,
        componentProps: {
          node,
        },
      });
      addUserFormDialog.onOk(() => {
        addUserFormDialog.hide();
        this.$emit('addUser')
      });
    },
    addNode(node) {
      const formComponent = sources.getNextForm(node.source);
      const source = sources.getNextSourceName(node.source);
      this.$q
        .dialog({
          component: formComponent,
          componentProps: {
            node,
          },
        })
        .onOk((data) => {
          this.$emit("addNode", { ...data, source }, node.division_id);
        });
    },
    confirmDeleteNode(node) {
      const dialog = this.$q.dialog({
        title: "Удаление пользователя",
        message: `Вы уверены, что хотите удалить ${node.title}?`,
        cancel: false,
      });
      dialog.onOk(() => {
        return sources
          .getApi(node.source)
          .delete(node.id)
          .then(() => {
            this.$notify("Успешно удалено", "positive");
            dialog.hide();
            this.$emit("deleteNode", node);
          })
          .catch(() => {
            this.$notify("Не удалось удалить");
          });
      });
    },
  },
});
</script>

<style scoped>
.left-side {
  height: 100%;
  padding: 10px;
  min-width: 240px;
  max-height: 100%;
  overflow-y: auto;
  background-color: var(--app-grey);
}
</style>
