"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { mockFeedback, mockTickets, mockActivities } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Clock, MessageSquare, Ticket } from "lucide-react"

export default function DashboardPage() {
  const totalFeedback = mockFeedback.length
  const openTickets = mockTickets.filter(t => t.status === "open").length
  const resolvedTickets = mockTickets.filter(t => t.status === "resolved").length
  const criticalIssues = mockFeedback.filter(f => f.priority === "critical").length

  const statCards = [
    { label: "Total Feedback", value: totalFeedback, icon: MessageSquare, trend: { value: "+12%", label: "vs last week", up: true } },
    { label: "Open Tickets", value: openTickets, icon: Ticket, trend: { value: "-5%", label: "vs last week", up: false } },
    { label: "Resolved Tickets", value: resolvedTickets, icon: CheckCircle, trend: { value: "+8%", label: "vs last week", up: true } },
    { label: "Critical Issues", value: criticalIssues, icon: AlertTriangle, meta: { value: "Avg. 2.5h to resolve", icon: Clock } },
  ]

  return (
    <div className="space-y-8 w-full">
      <div className="pt-2">
        <h1 className="text-3xl font-bold text-foreground">Dashboard Overview</h1>
        <p className="text-sm text-muted-foreground mt-2">Monitor your feedback intelligence at a glance</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {statCards.map((card) => (
          <Card key={card.label} className="border border-border hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">{card.label}</CardTitle>
              <card.icon className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">{card.value}</div>
              {card.trend ? (
                <div className="flex items-center gap-1 mt-2">
                  {card.trend.up
                    ? <TrendingUp className="h-3 w-3 text-emerald-500" />
                    : <TrendingDown className="h-3 w-3 text-red-500" />
                  }
                  <span className={`text-xs font-medium ${card.trend.up ? "text-emerald-500" : "text-red-500"}`}>
                    {card.trend.value}
                  </span>
                  <span className="text-xs text-muted-foreground">{card.trend.label}</span>
                </div>
              ) : card.meta ? (
                <div className="flex items-center gap-1.5 mt-2">
                  <card.meta.icon className="h-3 w-3 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">{card.meta.value}</span>
                </div>
              ) : null}
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="border border-border">
          <CardHeader className="pb-4">
            <CardTitle className="text-base font-semibold">Recent Feedback</CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs font-medium">Customer</TableHead>
                  <TableHead className="text-xs font-medium">Summary</TableHead>
                  <TableHead className="text-xs font-medium">Priority</TableHead>
                  <TableHead className="text-xs font-medium">Time</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockFeedback.slice(0, 5).map((feedback) => (
                  <TableRow key={feedback.id}>
                    <TableCell>
                      <div className="text-sm text-foreground">{feedback.customer.name}</div>
                      <div className="text-xs text-muted-foreground">{feedback.customer.company}</div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-foreground line-clamp-1 max-w-xs">{feedback.aiSummary}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={feedback.priority === "critical" ? "destructive" : feedback.priority === "high" ? "default" : "secondary"}>
                        {feedback.priority}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">{formatRelativeTime(feedback.createdAt)}</span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="border border-border">
          <CardHeader className="pb-4">
            <CardTitle className="text-base font-semibold">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-3">
              {mockActivities.slice(0, 5).map((activity) => (
                <div key={activity.id} className="flex items-start gap-3 pb-3 border-b border-border last:border-0 last:pb-0">
                  <Avatar className="h-8 w-8 shrink-0">
                    <AvatarFallback className="text-xs font-medium">{activity.userName.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground">{activity.description}</p>
                    <p className="text-xs text-muted-foreground mt-1">{formatRelativeTime(activity.createdAt)}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border border-border">
        <CardHeader className="pb-4">
          <CardTitle className="text-base font-semibold">AI Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-4">
            <li className="flex items-start gap-3">
              <span className="mt-2 h-2 w-2 rounded-full bg-primary flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-medium text-foreground">Dashboard performance issues are trending upward with 25 affected users</p>
                <p className="text-xs text-muted-foreground mt-1">Recommended: Investigate database queries and implement caching</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="mt-2 h-2 w-2 rounded-full bg-primary flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-medium text-foreground">High demand for dark mode feature across mobile platforms</p>
                <p className="text-xs text-muted-foreground mt-1">Recommended: Add to Q1 roadmap</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="mt-2 h-2 w-2 rounded-full bg-primary flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-medium text-foreground">Duplicate detection feature has reduced manual triage time by 40%</p>
                <p className="text-xs text-muted-foreground mt-1">Positive impact on team productivity</p>
              </div>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}