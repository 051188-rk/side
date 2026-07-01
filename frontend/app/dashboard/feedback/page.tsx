"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { PriorityBadge, SentimentBadge, StatusBadge, SourceBadge } from "@/components/ui/badge"
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

  const clearFilters = () => {
    setSearchQuery("")
    setFilterSource("")
    setFilterPriority("")
    setFilterStatus("")
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Feedback Inbox</h1>
        <p className="text-sm text-muted-foreground">Manage and analyze customer feedback from all channels</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Filters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search feedback..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9"
              />
            </div>
            <Select value={filterSource} onValueChange={(v) => v !== null && setFilterSource(v)}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="All Sources" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Sources</SelectItem>
                <SelectItem value="email">Email</SelectItem>
                <SelectItem value="discord">Discord</SelectItem>
                <SelectItem value="telegram">Telegram</SelectItem>
                <SelectItem value="github">GitHub</SelectItem>
                <SelectItem value="twitter">Twitter</SelectItem>
                <SelectItem value="bug_form">Bug Form</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterPriority} onValueChange={(v) => v !== null && setFilterPriority(v)}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="All Priorities" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Priorities</SelectItem>
                <SelectItem value="critical">Critical</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterStatus} onValueChange={(v) => v !== null && setFilterStatus(v)}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="All Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Status</SelectItem>
                <SelectItem value="open">Open</SelectItem>
                <SelectItem value="in_progress">In Progress</SelectItem>
                <SelectItem value="resolved">Resolved</SelectItem>
                <SelectItem value="closed">Closed</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" onClick={clearFilters}>
              <Filter className="h-4 w-4 mr-2" />
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
                <TableHead className="w-10" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredFeedback.map((feedback) => (
                <TableRow key={feedback.id}>
                  <TableCell>
                    <div className="text-sm text-foreground">{feedback.customer.name}</div>
                    <div className="text-xs text-muted-foreground">{feedback.customer.email}</div>
                  </TableCell>
                  <TableCell>
                    <SourceBadge source={feedback.source} />
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-foreground line-clamp-2 max-w-md">{feedback.aiSummary}</span>
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
                    <span className="text-xs text-muted-foreground whitespace-nowrap">{formatRelativeTime(feedback.createdAt)}</span>
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
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