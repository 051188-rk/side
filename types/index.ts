export type Priority = "critical" | "high" | "medium" | "low"
export type Status = "open" | "in_progress" | "resolved" | "closed"
export type Sentiment = "positive" | "neutral" | "negative"
export type Source = "email" | "discord" | "telegram" | "github" | "twitter" | "bug_form"
export type Category = "bug" | "feature" | "improvement" | "question" | "other"

export interface Customer {
  id: string
  name: string
  email: string
  avatar?: string
  company?: string
  createdAt: Date
}

export interface Feedback {
  id: string
  customerId: string
  customer: Customer
  source: Source
  rawMessage: string
  aiSummary: string
  detectedLanguage: string
  suggestedCategory: Category
  detectedSeverity: Priority
  sentiment: Sentiment
  status: Status
  priority: Priority
  createdAt: Date
  updatedAt: Date
  relatedFeedbackIds?: string[]
  ticketId?: string
}

export interface Ticket {
  id: string
  title: string
  description: string
  feedbackIds: string[]
  status: Status
  priority: Priority
  suggestedOwner?: string
  suggestedFixArea?: string
  reproductionSteps?: string[]
  duplicateReferences?: string[]
  affectedUsers: number
  createdAt: Date
  updatedAt: Date
  createdBy: string
  assignedTo?: string
  comments: Comment[]
  attachments: Attachment[]
}

export interface Comment {
  id: string
  ticketId: string
  authorId: string
  authorName: string
  content: string
  createdAt: Date
}

export interface Attachment {
  id: string
  ticketId: string
  fileName: string
  fileSize: number
  url: string
  uploadedAt: Date
  uploadedBy: string
}

export interface DuplicateCluster {
  id: string
  feedbackIds: string[]
  rootCause: string
  similarityScore: number
  affectedUsers: number
  status: Status
  createdAt: Date
  resolvedAt?: Date
}

export interface AIInsight {
  id: string
  type: "trending_bug" | "feature_request" | "recurring_issue" | "pain_point" | "complaint"
  title: string
  description: string
  affectedUsers: number
  frequency: number
  trend: "increasing" | "decreasing" | "stable"
  relatedFeedbackIds: string[]
  suggestedActions: string[]
  createdAt: Date
}

export interface AnalyticsData {
  sentimentTrend: {
    date: string
    positive: number
    neutral: number
    negative: number
  }[]
  channelDistribution: {
    source: Source
    count: number
    percentage: number
  }[]
  feedbackVolume: {
    date: string
    count: number
  }[]
  ticketGrowth: {
    date: string
    created: number
    resolved: number
  }[]
  resolutionTrends: {
    period: string
    avgResolutionTime: number
  }[]
  issueHeatmap: {
    category: Category
    severity: Priority
    count: number
  }[]
  priorityDistribution: {
    priority: Priority
    count: number
    percentage: number
  }[]
}

export interface ChannelIntegration {
  id: string
  type: Source
  name: string
  status: "connected" | "disconnected" | "error"
  lastSync: Date
  feedbackCount: number
  config: Record<string, any>
}

export interface Integration {
  id: string
  name: string
  type: "webhook" | "api" | "oauth"
  status: "active" | "inactive"
  config: Record<string, any>
  createdAt: Date
}

export interface Notification {
  id: string
  type: "info" | "warning" | "error" | "success"
  title: string
  message: string
  read: boolean
  createdAt: Date
  actionUrl?: string
}

export interface Activity {
  id: string
  type: "feedback_created" | "ticket_created" | "ticket_updated" | "cluster_created" | "comment_added"
  description: string
  userId: string
  userName: string
  entityId: string
  entityType: "feedback" | "ticket" | "cluster"
  createdAt: Date
}

export interface User {
  id: string
  name: string
  email: string
  role: "admin" | "manager" | "engineer" | "viewer"
  avatar?: string
  createdAt: Date
  lastActive: Date
}

export interface Organization {
  id: string
  name: string
  slug: string
  createdAt: Date
  plan: "free" | "pro" | "enterprise"
}

export interface MemoryItem {
  id: string
  type: "historical_bug" | "release_note" | "recurring_problem"
  title: string
  description: string
  date: Date
  relatedFeedbackIds: string[]
  resolution?: string
}

export interface FeedbackFilter {
  source?: Source
  priority?: Priority
  status?: Status
  sentiment?: Sentiment
  category?: Category
  search?: string
}
