export async function getHealth() {
  const response = await fetch('/api/health')
  if (!response.ok) throw new Error('后端健康检查失败')
  return response.json()
}
