"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { mockMemory } from "@/lib/data/mock-data"
import { formatDate } from "@/lib/utils"
import { History, BookOpen, AlertTriangle } from "lucide-react"

export default function MemoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Memory Explorer</h1>
        <p className="font-body text-ink-muted">Historical data and knowledge base</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockMemory.map((item) => {
          const icon = item.type === "historical_bug" ? AlertTriangle : item.type === "release_note" ? BookOpen : History
          
          return (
            <Card key={item.id}>
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-surface-2 rounded-lg">
                    <icon className="w-5 h-5 text-ink" />
                  </div>
                  <Badge variant="default">{item.type.replace("_", " ")}</Badge>
                </div>
                <CardTitle className="font-card-title">{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-body-sm text-ink-muted mb-4">{item.description}</p>
                
                {item.resolution && (
                  <div className="mb-4 p-3 bg-surface-2 rounded-md">
                    <p className="font-caption text-ink-muted mb-1">Resolution</p>
                    <p className="font-body-sm text-ink">{item.resolution}</p>
                  </div>
                )}
                
                <p className="font-caption text-ink-muted">{formatDate(item.date)}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <Card variant="surface-2">
        <CardContent className="p-12 text-center">
          <History className="w-16 h-16 text-ink-muted mx-auto mb-4" />
          <h3 className="font-headline text-ink mb-2">Knowledge Graph</h3>
          <p className="font-body text-ink-muted">Interactive knowledge graph visualization coming soon</p>
        </CardContent>
      </Card>
    </div>
  )
}
