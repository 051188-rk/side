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
    <div className="space-y-8 w-full">
      <div className="flex items-center justify-between pt-2">
        <div>
          <h1 className="text-foreground text-3xl font-bold">AI Insights</h1>
          <p className="text-muted-foreground mt-2">AI-generated insights from your feedback data</p>
        </div>
        <Button variant="default" size="sm" className="gap-2">
          <Brain className="w-4 h-4" />
          Generate Insights
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-max">
        {mockInsights.map((insight) => {
          const Icon = insightIcons[insight.type as keyof typeof insightIcons] || Brain

          return (
            <Card key={insight.id} className="border border-border hover:shadow-md transition-shadow h-full">
              <CardHeader className="px-6 pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2 bg-muted rounded-lg">
                    <Icon className="w-5 h-5 text-foreground" />
                  </div>
                  <Badge variant="secondary" className="capitalize text-xs">{insight.type.replace("_", " ")}</Badge>
                </div>
                <CardTitle className="text-base leading-snug">{insight.title}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 px-6 py-4">
                <p className="text-sm text-muted-foreground">{insight.description}</p>

                <div className="space-y-2.5 pt-2 border-t border-border">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Affected Users</span>
                    <span className="text-sm font-medium text-foreground">{insight.affectedUsers}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Frequency</span>
                    <span className="text-sm font-medium text-foreground">{insight.frequency}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground">Trend</span>
                    <span className={cn(
                      "text-sm flex items-center gap-1 font-medium",
                      insight.trend === "increasing" && "text-destructive",
                      insight.trend === "decreasing" && "text-emerald-500",
                      insight.trend === "stable" && "text-muted-foreground"
                    )}>
                      <TrendingUp className="w-3.5 h-3.5" />
                      {insight.trend}
                    </span>
                  </div>
                </div>

                <div className="pt-2 border-t border-border">
                  <p className="text-xs text-muted-foreground mb-2 font-medium">Suggested Actions</p>
                  <ul className="space-y-1.5">
                    {insight.suggestedActions.slice(0, 2).map((action, index) => (
                      <li key={index} className="text-sm text-foreground flex items-start gap-2">
                        <span className="text-primary text-xs mt-1.5">•</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <p className="text-xs text-muted-foreground pt-2 border-t border-border">{formatRelativeTime(insight.createdAt)}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}