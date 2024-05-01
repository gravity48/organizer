import { api } from "src/boot/axios"

export default {
  url: 'management-struct/',
  retrieve(source='root',source_id=1, indent=1) {
    return api.get(this.url, {params: { indent, source, source_id }})
  }
}
