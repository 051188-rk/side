"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge, PriorityBadge, StatusBadge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { mockTickets } from "@/lib/data/mock-data"
import { formatDateTime } from "@/lib/utils"
import { ArrowLeft, MessageSquare, Paperclip, Clock, User } from "lucide-react"
import Link from "next/link"

export default function TicketDetailPage({ params }: { params: { id: string } }) {
  const ticket = mockTickets.find(t => t.id === params.id)

  if (!ticket) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="font-body text-ink-muted">Ticket not found</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard/tickets">
          <Button variant="tertiary" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="font-display-lg text-ink">{ticket.title}</h1>
          <p className="font-body text-ink-muted">{ticket.id}</p>
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
              <CardTitle className="font-card-title">Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="font-body text-ink">{ticket.description}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="font-card-title">Reproduction Steps</CardTitle>
            </CardHeader>
            <CardContent>
              {ticket.reproductionSteps && ticket.reproductionSteps.length > 0 ? (
                <ol className="list-decimal list-inside space-y-2">
                  {ticket.reproductionSteps.map((step, index) => (
                    <li key={index} className="font-body-sm text-ink">{step}</li>
                  ))}
                </ol>
              ) : (
                <p className="font-body-sm text-ink-muted">No reproduction steps provided</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="font-card-title">Comments</CardTitle>
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
                    <div key={comment.id} className="flex gap-3 pb-4 border-b border-hairline-soft last:border-0 last:pb-0">
                      <div className="w-8 h-8 bg-surface-2 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="font-caption text-ink-muted">{comment.authorName.charAt(0)}</span>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-body-sm text-ink">{comment.authorName}</span>
                          <span className="font-caption text-ink-muted">{formatDateTime(comment.createdAt)}</span>
                        </div>
                        <p className="font-body-sm text-ink">{comment.content}</p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="font-body-sm text-ink-muted">No comments yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="font-card-title">Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="font-caption text-ink-muted mb-1">Created</p>
                <p className="font-body-sm text-ink">{formatDateTime(ticket.createdAt)}</p>
              </div>
              <div>
                <p className="font-caption text-ink-muted mb-1">Updated</p>
                <p className="font-body-sm text-ink">{formatDateTime(ticket.updatedAt)}</p>
              </div>
              <div>
                <p className="font-caption text-ink-muted mb-1">Assigned To</p>
                <p className="font-body-sm text-ink">{ticket.assignedTo || "Unassigned"}</p>
              </div>
              <div>
                <p className="font-caption text-ink-muted mb-1">Suggested Owner</p>
                <p className="font-body-sm text-ink">{ticket.suggestedOwner || "N/A"}</p>
              </div>
              <div>
                <p className="font-caption text-ink-muted mb-1">Suggested Fix Area</p>
                <p className="font-body-sm text-ink">{ticket.suggestedFixArea || "N/A"}</p>
              </div>
              <div>
                <p className="font-caption text-ink-muted mb-1">Affected Users</p>
                <p className="font-body-sm text-ink">{ticket.affectedUsers}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="font-card-title">Quick Actions</CardTitle>
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
