import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { mockTickets } from "@/lib/data/mock-data"
import { formatDateTime } from "@/lib/utils"
import { ArrowLeft, MessageSquare, Paperclip, Clock, User, ChevronLeft } from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

const priorityConfig: Record<string, { variant: "destructive" | "default" | "secondary" | "outline"; label: string }> = {
  critical: { variant: "destructive", label: "Critical" },
  high: { variant: "default", label: "High" },
  medium: { variant: "secondary", label: "Medium" },
  low: { variant: "outline", label: "Low" },
}

const statusConfig: Record<string, { variant: "default" | "secondary" | "outline"; label: string }> = {
  open: { variant: "default", label: "Open" },
  in_progress: { variant: "secondary", label: "In Progress" },
  closed: { variant: "outline", label: "Closed" },
}

function PriorityBadge({ priority }: { priority: string }) {
  const config = priorityConfig[priority] || { variant: "outline" as const, label: priority }
  return <Badge variant={config.variant}>{config.label}</Badge>
}

function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status] || { variant: "outline" as const, label: status }
  return <Badge variant={config.variant}>{config.label}</Badge>
}

export default async function TicketDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const ticket = mockTickets.find(t => t.id === id)

  if (!ticket) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-sm text-muted-foreground">Ticket not found</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard/tickets">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">{ticket.title}</h1>
          <p className="text-sm text-muted-foreground">{ticket.id}</p>
        </div>
        <div className="flex gap-2">
          <PriorityBadge priority={ticket.priority} />
          <StatusBadge status={ticket.status} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-foreground">{ticket.description}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Reproduction Steps</CardTitle>
            </CardHeader>
            <CardContent>
              {ticket.reproductionSteps && ticket.reproductionSteps.length > 0 ? (
                <ol className="list-decimal list-inside space-y-2">
                  {ticket.reproductionSteps.map((step, index) => (
                    <li key={index} className="text-sm text-foreground">{step}</li>
                  ))}
                </ol>
              ) : (
                <p className="text-sm text-muted-foreground">No reproduction steps provided</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Comments</CardTitle>
                <Button variant="secondary" size="sm">
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Add Comment
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {ticket.comments.length > 0 ? (
                  ticket.comments.map((comment) => (
                    <div key={comment.id} className="flex gap-3 pb-4 border-b border-border last:border-0 last:pb-0">
                      <Avatar size="sm">
                        <AvatarFallback>{comment.authorName.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm text-foreground">{comment.authorName}</span>
                          <span className="text-xs text-muted-foreground">{formatDateTime(comment.createdAt)}</span>
                        </div>
                        <p className="text-sm text-foreground">{comment.content}</p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-muted-foreground">No comments yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-xs text-muted-foreground mb-1">Created</p>
                <p className="text-sm text-foreground">{formatDateTime(ticket.createdAt)}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Updated</p>
                <p className="text-sm text-foreground">{formatDateTime(ticket.updatedAt)}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Assigned To</p>
                <p className="text-sm text-foreground">{ticket.assignedTo || "Unassigned"}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Suggested Owner</p>
                <p className="text-sm text-foreground">{ticket.suggestedOwner || "N/A"}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Suggested Fix Area</p>
                <p className="text-sm text-foreground">{ticket.suggestedFixArea || "N/A"}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Affected Users</p>
                <p className="text-sm text-foreground">{ticket.affectedUsers}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="secondary" className="w-full justify-start">
                <Clock className="w-4 h-4 mr-2" />
                Change Status
              </Button>
              <Button variant="secondary" className="w-full justify-start">
                <User className="w-4 h-4 mr-2" />
                Assign To
              </Button>
              <Button variant="secondary" className="w-full justify-start">
                <Paperclip className="w-4 h-4 mr-2" />
                Add Attachment
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
