import { Notification } from "@/types"
import { mockNotifications } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const notificationsApi = {
  getAll: async (): Promise<Notification[]> => {
    await delay(300)
    return [...mockNotifications]
  },

  markAsRead: async (id: string): Promise<boolean> => {
    await delay(200)
    const notification = mockNotifications.find(n => n.id === id)
    if (!notification) return false
    
    notification.read = true
    return true
  },

  markAllAsRead: async (): Promise<boolean> => {
    await delay(300)
    mockNotifications.forEach(n => n.read = true)
    return true
  },
}