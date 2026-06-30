import { Feedback, FeedbackFilter } from "@/types"
import { mockFeedback } from "@/lib/data/mock-data"

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const feedbackApi = {
  getAll: async (filters?: FeedbackFilter): Promise<Feedback[]> => {
    await delay(300)
    let filtered = [...mockFeedback]
    
    if (filters?.source) {
      filtered = filtered.filter(f => f.source === filters.source)
    }
    if (filters?.priority) {
      filtered = filtered.filter(f => f.priority === filters.priority)
    }
    if (filters?.status) {
      filtered = filtered.filter(f => f.status === filters.status)
    }
    if (filters?.sentiment) {
      filtered = filtered.filter(f => f.sentiment === filters.sentiment)
    }
    if (filters?.category) {
      filtered = filtered.filter(f => f.suggestedCategory === filters.category)
    }
    if (filters?.search) {
      const search = filters.search.toLowerCase()
      filtered = filtered.filter(f => 
        f.rawMessage.toLowerCase().includes(search) ||
        f.aiSummary.toLowerCase().includes(search)
      )
    }
    
    return filtered
  },

  getById: async (id: string): Promise<Feedback | null> => {
    await delay(200)
    return mockFeedback.find(f => f.id === id) || null
  },

  create: async (data: Partial<Feedback>): Promise<Feedback> => {
    await delay(400)
    const newFeedback: Feedback = {
      id: `f${Date.now()}`,
      customerId: data.customerId || "",
      customer: data.customer || mockFeedback[0].customer,
      source: data.source || "email",
      rawMessage: data.rawMessage || "",
      aiSummary: data.aiSummary || "",
      detectedLanguage: data.detectedLanguage || "en",
      suggestedCategory: data.suggestedCategory || "other",
      detectedSeverity: data.detectedSeverity || "medium",
      sentiment: data.sentiment || "neutral",
      status: data.status || "open",
      priority: data.priority || "medium",
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    mockFeedback.unshift(newFeedback)
    return newFeedback
  },

  update: async (id: string, data: Partial<Feedback>): Promise<Feedback | null> => {
    await delay(300)
    const index = mockFeedback.findIndex(f => f.id === id)
    if (index === -1) return null
    
    mockFeedback[index] = { ...mockFeedback[index], ...data, updatedAt: new Date() }
    return mockFeedback[index]
  },

  delete: async (id: string): Promise<boolean> => {
    await delay(200)
    const index = mockFeedback.findIndex(f => f.id === id)
    if (index === -1) return false
    
    mockFeedback.splice(index, 1)
    return true
  },
}

