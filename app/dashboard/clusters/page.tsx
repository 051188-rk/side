"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { Progress } from "@/components/ui/progress"
import { mockClusters } from "@/lib/data/mock-data"
import { formatRelativeTime, cn } from "@/lib/utils"
import { GitMerge } from "lucide-react"

export default function ClustersPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-foreground text-2xl font-semibold mb-1">Duplicate Clusters</h1>
        <p className="text-muted-foreground">AI-detected duplicate feedback grouped by similarity</p>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Cluster ID</TableHead>
                <TableHead>Root Cause</TableHead>
                <TableHead>Feedback Count</TableHead>
                <TableHead>Similarity Score</TableHead>
                <TableHead>Affected Users</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Created</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockClusters.map((cluster) => (
                <TableRow key={cluster.id}>
                  <TableCell>
                    <span className="text-sm text-muted-foreground">{cluster.id}</span>
                  </TableCell>
                  <TableCell>
                    <div className="text-sm">{cluster.rootCause}</div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{cluster.feedbackIds.length}</span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Progress value={cluster.similarityScore * 100} className="w-16" />
                      <span className="text-xs text-muted-foreground">{Math.round(cluster.similarityScore * 100)}%</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{cluster.affectedUsers}</span>
                  </TableCell>
                  <TableCell>
                    <Badge className={cn(
                      "capitalize",
                      cluster.status === "open" && "bg-destructive/10 text-destructive hover:bg-destructive/20",
                      cluster.status === "resolved" && "bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20"
                    )}>
                      {cluster.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <span className="text-xs text-muted-foreground">{formatRelativeTime(cluster.createdAt)}</span>
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
