import { api } from "src/boot/axios";

export default {
  baseUrl: "administration",
  update(pk, patchData) {
    return api.patch(`${this.baseUrl}/${pk}/`, patchData);
  },
  create(data) {
    return api.post(`${this.baseUrl}/`, data);
  },
  delete(pk) {
    return api.delete(`${this.baseUrl}/${pk}/`);
  },
  getStatistic(pk) {
    return api.get(`${this.baseUrl}/${pk}/stat/`);
  },
};
