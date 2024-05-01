<template>
  <q-page class="flex flex-start">
    <div class="page-wrapper">
      <left-side
        :tree="managementStructList"
        v-model:treeNodeClicked="clickedNode"
        @on-lazy-load="onLazyLoad"
        @update-node="updateNode"
        @add-node="addNode"
        @deleteNode="deleteNode"
        @update:treeNodeClicked="onNodeClick"
        @add-user="onNodeClick"
      />
      <div class="full-width">
        <statistic-node
          :count="statistic.count"
          :avg-year="statistic.avgYear"
          :avg-exp="statistic.avgExp"
          :loading="statisticLoading"
        />
        <user-card-list
          @delete-user="confirmDeleteUser"
          @update-user="updateUser"
          :loading="employeeLoading"
          :users="users"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import LeftSide from "../components/indexPageComponents/LeftSide.vue";
import UserCardList from "../components/indexPageComponents/UserCardList.vue";
import managementStructApi from "../services/managementStruct";
import employee from "src/services/employee";
import UserForm from "../components/forms/UserForm.vue";
import sources from "src/domain/managementStrcut";
import StatisticNode from "src/components/indexPageComponents/StatisticNode.vue";

export default defineComponent({
  name: "IndexPage",
  components: {
    LeftSide,
    UserCardList,
    StatisticNode,
  },
  data() {
    return {
      clickedNode: {},
      users: [],
      managementStructList: [],
      employeeLoading: false,
      statisticLoading: false,
      statistic: {
        count: 0,
        avgYear: null,
        avgExpt: null,
      },
    };
  },
  methods: {
    updateUser(user) {
      const dialog = this.$q.dialog({
        component: UserForm,
        componentProps: {
          user,
          isPatch: true,
        },
      });
      dialog.onOk(() => {
        dialog.hide();
        this.onNodeClick();
      });
    },
    updateNodeInManagementStructList(nodeList, node) {
      nodeList.forEach((item, index) => {
        if (item.division_id === node.division_id) {
          nodeList[index].title = node.title;
          return;
        } else if (nodeList[index].children) {
          this.updateNodeInManagementStructList(nodeList[index].children, node);
        }
      });
    },
    onNodeClick() {
      if (this.clickedNode.source === "root") return;
      Promise.all([this.filterEmployeeByNode(), this.getStatistic()]);
    },
    getStatistic() {
      this.statisticLoading = true;
      sources
        .getApi(this.clickedNode.source)
        .getStatistic(this.clickedNode.id)
        .then(({ data }) => {
          this.statistic.count = data.employee_count;
          this.statistic.avgYear = data.employee_avg_year;
          this.statistic.avgExp = data.employee_avg_exp;
        })
        .catch(() => {
          this.$notify("Не удалось загрузить статистику");
        })
        .finally(() => {
          this.statisticLoading = false;
        });
    },
    filterEmployeeByNode() {
      this.employeeLoading = true;
      return employee
        .filter({ division_id: this.clickedNode.division_id })
        .then(({ data }) => {
          this.users = data;
        })
        .catch(() => {
          this.$notify("Не удалось загрузить employee");
        })
        .finally(() => {
          this.employeeLoading = false;
        });
    },
    updateNode(node) {
      this.updateNodeInManagementStructList(this.managementStructList, node);
    },
    addNodeInManagementStructList(nodeList, node, divisionId) {
      nodeList.forEach((item, index) => {
        if (item.division_id === divisionId) {
          if (nodeList[index].children) {
            nodeList[index].children.push(node);
            return;
          }
          nodeList[index].children = [node];
          return;
        } else if (nodeList[index].children) {
          this.addNodeInManagementStructList(
            nodeList[index].children,
            node,
            divisionId
          );
        }
      });
    },
    addNode(node, divisionId) {
      this.addNodeInManagementStructList(
        this.managementStructList,
        node,
        divisionId
      );
    },
    onLazyLoad({ node, key, done, fail }) {
      return managementStructApi
        .retrieve(node.source, node.id)
        .then(({ data }) => {
          done(
            data.children.map((item) => {
              item.label = item.title;
              if (item.source != "group") {
                item.lazy = true;
              } else {
                item.isLeaf = true;
              }
              return item;
            })
          );
        });
    },
    confirmDeleteUser(user) {
      this.$q
        .dialog({
          title: "Удаление пользователя",
          message: `Вы уверены, что хотите удалить ${user.full_name}?`,
          cancel: true,
        })
        .onOk(() => {
          return employee
            .delete(user.id)
            .then(() => {
              this.users.splice(
                this.users.findIndex(
                  (employeeUser) => employeeUser.id === user.id
                ),
                1
              );
              this.onNodeClick();
            })
            .catch(() => {
              this.$notify("Не удалось удалить эмплойе");
            });
        });
    },
    deleteNodeFromManagementStructList(nodeList, node) {
      nodeList.forEach((item, index) => {
        if (item.division_id === node.division_id) {
          nodeList.splice(index, 1);
          return;
        } else if (nodeList[index].children) {
          this.deleteNodeFromManagementStructList(
            nodeList[index].children,
            node
          );
        }
      });
    },
    deleteNode(node) {
      this.deleteNodeFromManagementStructList(this.managementStructList, node);
      this.onNodeClick();
    },
    pushChildrensToManagementStruct(data) {
      if (data.source === "root") {
        this.managementStructList.push({
          title: data.title,
          source: data.source,
          id: data.id,
          division_id: new Date().getTime(),
          children: data.children.map((item) => {
            item.lazy = true;
            return item;
          }),
        });
        return;
      }
    },
    getManagementStruct(service, id) {
      return managementStructApi
        .retrieve(service, id)
        .then(({ data }) => this.pushChildrensToManagementStruct(data))
        .catch((e) => {
          this.$notify("Не удалось получить дерево подразделений");
        });
    },
  },
  async created() {
    await this.getManagementStruct("root", 1);
  },
});
</script>
<style scoped>
.page-wrapper {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: row;
  overflow: hidden;
}
</style>
