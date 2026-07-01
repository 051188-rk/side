import { AIInsight } from "@/types"
import { mockInsights } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const insightsApi = {
  getAll: async (): Promise<AIInsight[]> => {
    await delay(300)
    return [...mockInsights]
  },

  getById: async (id: string): Promise<AIInsight | null> => {
    await delay(200)
    return mockInsights.find(i => i.id === id) || null
  },

  getByType: async (type: string): Promise<AIInsight[]> => {
    await delay(300)
    return mockInsights.filter(i => i.type === type)
  },
}