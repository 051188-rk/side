"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { mockMemory } from "@/lib/data/mock-data"
import { formatDate } from "@/lib/utils"
import { History, BookOpen, AlertTriangle } from "lucide-react"

export default function MemoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Memory Explorer</h1>
        <p className="text-sm text-muted-foreground">Historical data and knowledge base</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockMemory.map((item) => {
          const Icon = item.type === "historical_bug" ? AlertTriangle : item.type === "release_note" ? BookOpen : History

          return (
            <Card key={item.id}>
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-muted rounded-lg">
                    <Icon className="w-5 h-5 text-foreground" />
                  </div>
                  <Badge variant="secondary">{item.type.replace("_", " ")}</Badge>
                </div>
                <CardTitle>{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">{item.description}</p>

                {item.resolution && (
                  <div className="mb-4 p-3 bg-muted rounded-md">
                    <p className="text-xs text-muted-foreground mb-1">Resolution</p>
                    <p className="text-sm text-foreground">{item.resolution}</p>
                  </div>
                )}

                <p className="text-xs text-muted-foreground">{formatDate(item.date)}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <Card>
        <CardContent className="py-12 text-center">
          <History className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-foreground mb-2">Knowledge Graph</h3>
          <p className="text-sm text-muted-foreground">Interactive knowledge graph visualization coming soon</p>
        </CardContent>
      </Card>
    </div>
  )
}