import { DuplicateCluster } from "@/types"
import { mockClusters } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const clustersApi = {
  getAll: async (): Promise<DuplicateCluster[]> => {
    await delay(300)
    return [...mockClusters]
  },

  getById: async (id: string): Promise<DuplicateCluster | null> => {
    await delay(200)
    return mockClusters.find(c => c.id === id) || null
  },

  create: async (data: Partial<DuplicateCluster>): Promise<DuplicateCluster> => {
    await delay(400)
    const newCluster: DuplicateCluster = {
      id: `c${Date.now()}`,
      feedbackIds: data.feedbackIds || [],
      rootCause: data.rootCause || "",
      similarityScore: data.similarityScore || 0,
      affectedUsers: data.affectedUsers || 0,
      status: data.status || "open",
      createdAt: new Date(),
      resolvedAt: data.resolvedAt,
    }
    mockClusters.unshift(newCluster)
    return newCluster
  },

  update: async (id: string, data: Partial<DuplicateCluster>): Promise<DuplicateCluster | null> => {
    await delay(300)
    const index = mockClusters.findIndex(c => c.id === id)
    if (index === -1) return null
    
    mockClusters[index] = { ...mockClusters[index], ...data }
    return mockClusters[index]
  },
}