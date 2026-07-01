"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { mockInsights } from "@/lib/data/mock-data"
import { formatRelativeTime, cn } from "@/lib/utils"
import { Brain, TrendingUp, Lightbulb, AlertCircle } from "lucide-react"

const insightIcons = {
  trending_bug: AlertCircle,
  feature_request: Lightbulb,
  pain_point: Brain,
} as const

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-foreground text-2xl font-semibold mb-1">AI Insights</h1>
          <p className="text-muted-foreground">AI-generated insights from your feedback data</p>
        </div>
        <Button variant="outline" size="sm">
          <Brain className="w-4 h-4" />
          Generate Insights
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockInsights.map((insight) => {
          const Icon = insightIcons[insight.type as keyof typeof insightIcons] || Brain

          return (
            <Card key={insight.id}>
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-muted rounded-lg">
                    <Icon className="w-5 h-5 text-foreground" />
                  </div>
                  <Badge variant="secondary" className="capitalize">{insight.type.replace("_", " ")}</Badge>
                </div>
                <CardTitle>{insight.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">{insight.description}</p>

                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Affected Users</span>
                    <span className="text-sm text-foreground">{insight.affectedUsers}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Frequency</span>
                    <span className="text-sm text-foreground">{insight.frequency}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Trend</span>
                    <span className={cn(
                      "text-sm flex items-center gap-1",
                      insight.trend === "increasing" && "text-destructive",
                      insight.trend === "decreasing" && "text-emerald-500",
                      insight.trend === "stable" && "text-muted-foreground"
                    )}>
                      <TrendingUp className="w-4 h-4" />
                      {insight.trend}
                    </span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-border">
                  <p className="text-xs text-muted-foreground mb-2">Suggested Actions</p>
                  <ul className="space-y-1">
                    {insight.suggestedActions.slice(0, 2).map((action, index) => (
                      <li key={index} className="text-sm text-foreground flex items-start gap-2">
                        <span className="text-primary">•</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>

                <p className="text-xs text-muted-foreground mt-4">{formatRelativeTime(insight.createdAt)}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}