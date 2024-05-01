export function required(val) {
  if (val === '' || val === null) {
    return 'Поле обязательно'
  }
  return true
}
