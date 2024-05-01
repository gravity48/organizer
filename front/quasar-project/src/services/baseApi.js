import { api } from "src/boot/axios"

class BaseCRUDApi {
  constructor(url) {
    this.baseUrl = url
  }
  list(params) {
    return api.get(`${this.baseUrl}/`, {params})
  }
  retrieve(pk) {
    return api.get(`${this.baseUrl}/${pk}/`)
  }

}
