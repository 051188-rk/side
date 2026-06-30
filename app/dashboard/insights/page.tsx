"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { mockInsights } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Brain, TrendingUp, Lightbulb, AlertCircle } from "lucide-react"

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">AI Insights</h1>
        <p className="font-body text-ink-muted">AI-generated insights from your feedback data</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockInsights.map((insight) => {
          const icon = insight.type === "trending_bug" ? AlertCircle : insight.type === "feature_request" ? Lightbulb : Brain
          const trendColor = insight.trend === "increasing" ? "text-semantic-error" : insight.trend === "decreasing" ? "text-semantic-success" : "text-ink-muted"
          
          return (
            <Card key={insight.id}>
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-surface-2 rounded-lg">
                    <icon className="w-5 h-5 text-ink" />
                  </div>
                  <Badge variant="default">{insight.type.replace("_", " ")}</Badge>
                </div>
                <CardTitle className="font-card-title">{insight.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-body-sm text-ink-muted mb-4">{insight.description}</p>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="font-caption text-ink-muted">Affected Users</span>
                    <span className="font-body-sm text-ink">{insight.affectedUsers}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-caption text-ink-muted">Frequency</span>
                    <span className="font-body-sm text-ink">{insight.frequency}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-caption text-ink-muted">Trend</span>
                    <span className={`font-body-sm ${trendColor} flex items-center gap-1`}>
                      <TrendingUp className="w-4 h-4" />
                      {insight.trend}
                    </span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-hairline-soft">
                  <p className="font-caption text-ink-muted mb-2">Suggested Actions</p>
                  <ul className="space-y-1">
                    {insight.suggestedActions.slice(0, 2).map((action, index) => (
                      <li key={index} className="font-body-sm text-ink flex items-start gap-2">
                        <span className="text-accent-blue">•</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>

                <p className="font-caption text-ink-muted mt-4">{formatRelativeTime(insight.createdAt)}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
