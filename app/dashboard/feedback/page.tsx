"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge, PriorityBadge, SentimentBadge, StatusBadge, SourceBadge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { mockFeedback } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Filter, Search, MoreHorizontal } from "lucide-react"

export default function FeedbackPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [filterSource, setFilterSource] = useState("")
  const [filterPriority, setFilterPriority] = useState("")
  const [filterStatus, setFilterStatus] = useState("")

  const filteredFeedback = mockFeedback.filter(f => {
    if (searchQuery && !f.rawMessage.toLowerCase().includes(searchQuery.toLowerCase()) && !f.aiSummary.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false
    }
    if (filterSource && f.source !== filterSource) return false
    if (filterPriority && f.priority !== filterPriority) return false
    if (filterStatus && f.status !== filterStatus) return false
    return true
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Feedback Inbox</h1>
        <p className="font-body text-ink-muted">Manage and analyze customer feedback from all channels</p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="font-card-title">Filters</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-muted" />
              <Input
                placeholder="Search feedback..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <select
              value={filterSource}
              onChange={(e) => setFilterSource(e.target.value)}
              className="input-field"
            >
              <option value="">All Sources</option>
              <option value="email">Email</option>
              <option value="discord">Discord</option>
              <option value="telegram">Telegram</option>
              <option value="github">GitHub</option>
              <option value="twitter">Twitter</option>
              <option value="bug_form">Bug Form</option>
            </select>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="input-field"
            >
              <option value="">All Priorities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="input-field"
            >
              <option value="">All Status</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
            <Button variant="secondary" onClick={() => { setSearchQuery(""); setFilterSource(""); setFilterPriority(""); setFilterStatus("") }}>
              <Filter className="w-4 h-4 mr-2" />
              Clear Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Customer</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Summary</TableHead>
                <TableHead>Sentiment</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Time</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredFeedback.map((feedback) => (
                <TableRow key={feedback.id}>
                  <TableCell>
                    <div className="font-body-sm">{feedback.customer.name}</div>
                    <div className="font-caption text-ink-muted">{feedback.customer.email}</div>
                  </TableCell>
                  <TableCell>
                    <SourceBadge source={feedback.source} />
                  </TableCell>
                  <TableCell>
                    <div className="font-body-sm max-w-md">{feedback.aiSummary}</div>
                  </TableCell>
                  <TableCell>
                    <SentimentBadge sentiment={feedback.sentiment} />
                  </TableCell>
                  <TableCell>
                    <PriorityBadge priority={feedback.priority} />
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={feedback.status} />
                  </TableCell>
                  <TableCell>
                    <span className="font-caption text-ink-muted">{formatRelativeTime(feedback.createdAt)}</span>
                  </TableCell>
                  <TableCell>
                    <button className="p-1 hover:bg-surface-1 rounded">
                      <MoreHorizontal className="w-4 h-4 text-ink-muted" />
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
