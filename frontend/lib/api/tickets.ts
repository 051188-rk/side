import { Ticket, Comment } from "@/types"
import { mockTickets } from "@/lib/data/mock-data"

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const ticketsApi = {
  getAll: async (): Promise<Ticket[]> => {
    await delay(300)
    return [...mockTickets]
  },

  getById: async (id: string): Promise<Ticket | null> => {
    await delay(200)
    return mockTickets.find(t => t.id === id) || null
  },

  create: async (data: Partial<Ticket>): Promise<Ticket> => {
    await delay(400)
    const newTicket: Ticket = {
      id: `t${Date.now()}`,
      title: data.title || "",
      description: data.description || "",
      feedbackIds: data.feedbackIds || [],
      status: data.status || "open",
      priority: data.priority || "medium",
      suggestedOwner: data.suggestedOwner,
      suggestedFixArea: data.suggestedFixArea,
      reproductionSteps: data.reproductionSteps,
      duplicateReferences: data.duplicateReferences,
      affectedUsers: data.affectedUsers || 0,
      createdAt: new Date(),
      updatedAt: new Date(),
      createdBy: data.createdBy || "system",
      assignedTo: data.assignedTo,
      comments: data.comments || [],
      attachments: data.attachments || [],
    }
    mockTickets.unshift(newTicket)
    return newTicket
  },

  update: async (id: string, data: Partial<Ticket>): Promise<Ticket | null> => {
    await delay(300)
    const index = mockTickets.findIndex(t => t.id === id)
    if (index === -1) return null
    
    mockTickets[index] = { ...mockTickets[index], ...data, updatedAt: new Date() }
    return mockTickets[index]
  },

  delete: async (id: string): Promise<boolean> => {
    await delay(200)
    const index = mockTickets.findIndex(t => t.id === id)
    if (index === -1) return false
    
    mockTickets.splice(index, 1)
    return true
  },

  addComment: async (ticketId: string, comment: Omit<Comment, "id" | "ticketId">): Promise<Comment> => {
    await delay(200)
    const ticket = mockTickets.find(t => t.id === ticketId)
    if (!ticket) throw new Error("Ticket not found")
    
    const newComment: Comment = {
      id: `c${Date.now()}`,
      ticketId,
      ...comment,
    }
    ticket.comments.push(newComment)
    return newComment
  },
}