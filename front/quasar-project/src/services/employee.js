import { api } from "src/boot/axios"

export default {
  baseUrl: 'employee',
  update(pk, patchData) {
    return api.put(`${this.baseUrl}/${pk}/`,patchData, {
      headers: { "Content-Type": "multipart/form-data" }
    })
  },
  create(data) {
    return api.post(`${this.baseUrl}/`, data, {
      headers: { "Content-Type": "multipart/form-data" }
    })
  },
  delete(pk) {
    return api.delete(`${this.baseUrl}/${pk}/`)
  },
  filter(params={}) {
    return api.get(`${this.baseUrl}/`, {params})
  }
}
