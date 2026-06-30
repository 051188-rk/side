"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge, PriorityBadge, StatusBadge } from "@/components/ui/badge"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { mockTickets } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Plus, MoreHorizontal } from "lucide-react"

export default function TicketsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display-lg text-ink mb-2">Tickets</h1>
          <p className="font-body text-ink-muted">Track and manage support tickets</p>
        </div>
        <Button variant="primary">
          <Plus className="w-4 h-4 mr-2" />
          New Ticket
        </Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Assigned To</TableHead>
                <TableHead>Affected Users</TableHead>
                <TableHead>Created</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockTickets.map((ticket) => (
                <TableRow key={ticket.id}>
                  <TableCell>
                    <span className="font-body-sm text-ink-muted">{ticket.id}</span>
                  </TableCell>
                  <TableCell>
                    <div className="font-body-sm">{ticket.title}</div>
                    <div className="font-caption text-ink-muted">{ticket.description.slice(0, 50)}...</div>
                  </TableCell>
                  <TableCell>
                    <PriorityBadge priority={ticket.priority} />
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={ticket.status} />
                  </TableCell>
                  <TableCell>
                    <span className="font-body-sm">{ticket.assignedTo || "Unassigned"}</span>
                  </TableCell>
                  <TableCell>
                    <span className="font-body-sm">{ticket.affectedUsers}</span>
                  </TableCell>
                  <TableCell>
                    <span className="font-caption text-ink-muted">{formatRelativeTime(ticket.createdAt)}</span>
                  </TableCell>
                  <TableCell>
                    <button className="p-1 hover:bg-surface-1 rounded">
                      <MoreHorizontal className="w-4 h-4 text-ink-muted" />
                    </button>
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
