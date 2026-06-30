import { ChannelIntegration } from "@/types"
import { mockChannels } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const channelsApi = {
  getAll: async (): Promise<ChannelIntegration[]> => {
    await delay(300)
    return [...mockChannels]
  },

  getById: async (id: string): Promise<ChannelIntegration | null> => {
    await delay(200)
    return mockChannels.find(c => c.id === id) || null
  },

  update: async (id: string, data: Partial<ChannelIntegration>): Promise<ChannelIntegration | null> => {
    await delay(300)
    const index = mockChannels.findIndex(c => c.id === id)
    if (index === -1) return null
    
    mockChannels[index] = { ...mockChannels[index], ...data, lastSync: new Date() }
    return mockChannels[index]
  },
}
