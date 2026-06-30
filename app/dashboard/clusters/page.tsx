"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge, StatusBadge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { mockClusters } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { GitMerge } from "lucide-react"

export default function ClustersPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Duplicate Clusters</h1>
        <p className="font-body text-ink-muted">AI-detected duplicate feedback grouped by similarity</p>
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
                    <span className="font-body-sm text-ink-muted">{cluster.id}</span>
                  </TableCell>
                  <TableCell>
                    <div className="font-body-sm">{cluster.rootCause}</div>
                  </TableCell>
                  <TableCell>
                    <span className="font-body-sm">{cluster.feedbackIds.length}</span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-surface-2 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-accent-blue" 
                          style={{ width: `${cluster.similarityScore * 100}%` }}
                        />
                      </div>
                      <span className="font-caption text-ink-muted">{Math.round(cluster.similarityScore * 100)}%</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="font-body-sm">{cluster.affectedUsers}</span>
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={cluster.status} />
                  </TableCell>
                  <TableCell>
                    <span className="font-caption text-ink-muted">{formatRelativeTime(cluster.createdAt)}</span>
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
