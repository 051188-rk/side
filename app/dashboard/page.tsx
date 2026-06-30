"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { mockFeedback, mockTickets, mockActivities } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Clock, MessageSquare, Ticket as TicketIcon } from "lucide-react"

export default function DashboardPage() {
  const totalFeedback = mockFeedback.length
  const openTickets = mockTickets.filter(t => t.status === "open").length
  const resolvedTickets = mockTickets.filter(t => t.status === "resolved").length
  const criticalIssues = mockFeedback.filter(f => f.priority === "critical").length

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-medium text-text-primary mb-2">Dashboard Overview</h1>
        <p className="text-sm text-text-secondary">Monitor your feedback intelligence at a glance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="bg-surface border border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-text-primary">Total Feedback</CardTitle>
              <MessageSquare className="w-4 h-4 text-text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-medium text-text-primary">{totalFeedback}</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp className="w-3 h-3 text-text-secondary" />
              <span className="text-xs text-text-secondary">+12%</span>
              <span className="text-xs text-text-tertiary">vs last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-surface border border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-text-primary">Open Tickets</CardTitle>
              <TicketIcon className="w-4 h-4 text-text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-medium text-text-primary">{openTickets}</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingDown className="w-3 h-3 text-text-secondary" />
              <span className="text-xs text-text-secondary">-5%</span>
              <span className="text-xs text-text-tertiary">vs last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-surface border border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-text-primary">Resolved Tickets</CardTitle>
              <CheckCircle className="w-4 h-4 text-text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-medium text-text-primary">{resolvedTickets}</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp className="w-3 h-3 text-text-secondary" />
              <span className="text-xs text-text-secondary">+8%</span>
              <span className="text-xs text-text-tertiary">vs last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-surface border border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-text-primary">Critical Issues</CardTitle>
              <AlertTriangle className="w-4 h-4 text-text-secondary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-medium text-text-primary">{criticalIssues}</div>
            <div className="flex items-center gap-1 mt-2">
              <Clock className="w-3 h-3 text-text-tertiary" />
              <span className="text-xs text-text-tertiary">Avg. 2.5h to resolve</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <Card className="bg-surface border border-border">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-text-primary">Recent Feedback</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs text-text-secondary">Customer</TableHead>
                  <TableHead className="text-xs text-text-secondary">Summary</TableHead>
                  <TableHead className="text-xs text-text-secondary">Priority</TableHead>
                  <TableHead className="text-xs text-text-secondary">Time</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockFeedback.slice(0, 5).map((feedback) => (
                  <TableRow key={feedback.id}>
                    <TableCell>
                      <div className="text-xs text-text-primary">{feedback.customer.name}</div>
                      <div className="text-xs text-text-tertiary">{feedback.customer.company}</div>
                    </TableCell>
                    <TableCell>
                      <div className="text-xs text-text-primary max-w-xs truncate">{feedback.aiSummary}</div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={feedback.priority === "critical" ? "error" : feedback.priority === "high" ? "warning" : "default"}>
                        {feedback.priority}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-xs text-text-tertiary">{formatRelativeTime(feedback.createdAt)}</span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="bg-surface border border-border">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-text-primary">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockActivities.slice(0, 5).map((activity) => (
                <div key={activity.id} className="flex items-start gap-3 pb-4 border-b border-border last:border-0 last:pb-0">
                  <div className="w-8 h-8 border border-border flex items-center justify-center flex-shrink-0">
                    <span className="text-xs text-text-secondary">{activity.userName.charAt(0)}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-text-primary">{activity.description}</p>
                    <p className="text-xs text-text-tertiary mt-1">{formatRelativeTime(activity.createdAt)}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-surface border border-border">
        <CardHeader>
          <CardTitle className="text-sm font-medium text-text-primary">AI Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-text-secondary rounded-full mt-2 flex-shrink-0" />
              <div>
                <p className="text-xs text-text-primary">Dashboard performance issues are trending upward with 25 affected users</p>
                <p className="text-xs text-text-tertiary mt-1">Recommended: Investigate database queries and implement caching</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-text-secondary rounded-full mt-2 flex-shrink-0" />
              <div>
                <p className="text-xs text-text-primary">High demand for dark mode feature across mobile platforms</p>
                <p className="text-xs text-text-tertiary mt-1">Recommended: Add to Q1 roadmap</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-text-secondary rounded-full mt-2 flex-shrink-0" />
              <div>
                <p className="text-xs text-text-primary">Duplicate detection feature has reduced manual triage time by 40%</p>
                <p className="text-xs text-text-tertiary mt-1">Positive impact on team productivity</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
