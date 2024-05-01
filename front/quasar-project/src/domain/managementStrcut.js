import AdministrationForm from "components/forms/AdministrationForm.vue";
import ServiceForm from "components/forms/ServiceForm.vue";
import GroupForm from "components/forms/GroupForm.vue";
import DepartmentForm from "components/forms/DepartmentForm.vue";
import administration from "src/services/administration";
import group from "src/services/group";
import service from "src/services/service";
import department from "src/services/department";

class BaseSource {
  constructor(name, form, api) {
    this.name = name
    this.form = form
    this.api = api
  }
}

class Sources {
  constructor() {
    this.nodeDict = {};
    this.head = null;
  }
  addNode(name, form = null, api) {
    this.nodeDict[name] = new BaseSource(name, form, api);
    if (this.head != null) {
      this.head.next = this.nodeDict[name];
      this.nodeDict[name].prev = this.head;
    }
    this.head = this.nodeDict[name];
    return this;
  }
  getNodeByName(nodeName) {
    return this.nodeDict[nodeName];
  }
  getForm(nodeName) {
    return this.nodeDict[nodeName].form;
  }
  getNextForm(nodeName) {
    return this.nodeDict[nodeName].next.form;
  }
  getNextSourceName(nodeName) {
    return this.nodeDict[nodeName].next.name
  }
  getApi(nodeName) {
    return this.nodeDict[nodeName].api
  }
}

const sources = new Sources();

sources
  .addNode("root")
  .addNode("service", ServiceForm, service)
  .addNode("administration", AdministrationForm, administration)
  .addNode("department", DepartmentForm, department)
  .addNode("group", GroupForm, group);

export default sources;
