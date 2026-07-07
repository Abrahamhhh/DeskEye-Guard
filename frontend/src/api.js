const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(path, { token, headers = {}, ...options } = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const error = new Error(data.detail || `请求失败（${response.status}）`)
    error.status = response.status
    throw error
  }
  return data
}

export const loginApi = (payload) => request('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) })
export const registerApi = (payload) => request('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) })
export const meApi = (token) => request('/api/auth/me', { token })
export const changePasswordApi = (token, payload) => request('/api/auth/change-password', { token, method: 'POST', body: JSON.stringify(payload) })
export const todayStatsApi = (token) => request('/api/stats/today', { token })
export const recentEventsApi = (token, limit = 20) => request(`/api/events/recent?limit=${limit}`, { token })
export const postureTrendApi = (token, days = 7) => request(`/api/stats/posture-trend?days=${days}`, { token })
export const adminDevicesApi = (token) => request('/api/admin/devices', { token })
export const adminEventsApi = (token) => request('/api/admin/events', { token })
export const adminSummaryApi = (token) => request('/api/admin/summary', { token })

// ESP32-S3 或设备模拟脚本使用此方法，浏览器页面本身不会调用。
export const submitDeviceEventApi = (deviceKey, payload) => request('/api/device/events', {
  method: 'POST',
  headers: { 'X-Device-Key': deviceKey },
  body: JSON.stringify(payload),
})
