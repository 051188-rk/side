import { AnalyticsData } from "@/types"
import { mockAnalytics } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const analyticsApi = {
  getAnalytics: async (): Promise<AnalyticsData> => {
    await delay(400)
    return { ...mockAnalytics }
  },
}