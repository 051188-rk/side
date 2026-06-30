"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge, StatusBadge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { mockChannels } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Mail, MessageSquare, Send, Github, Twitter, FileText, Zap, Settings } from "lucide-react"

const channelIcons: Record<string, any> = {
  email: Mail,
  discord: MessageSquare,
  telegram: Send,
  github: Github,
  twitter: Twitter,
  bug_form: FileText,
}

export default function ChannelsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Channels</h1>
        <p className="font-body text-ink-muted">Manage feedback source integrations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockChannels.map((channel) => {
          const Icon = channelIcons[channel.type] || Zap
          
          return (
            <Card key={channel.id}>
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-surface-2 rounded-lg">
                    <Icon className="w-5 h-5 text-ink" />
                  </div>
                  <StatusBadge status={channel.status === "connected" ? "open" : "closed"} />
                </div>
                <CardTitle className="font-card-title">{channel.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="font-caption text-ink-muted">Last Sync</span>
                    <span className="font-body-sm text-ink">{formatRelativeTime(channel.lastSync)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-caption text-ink-muted">Feedback Count</span>
                    <span className="font-body-sm text-ink">{channel.feedbackCount}</span>
                  </div>
                </div>

                <div className="mt-4 flex gap-2">
                  <Button variant="secondary" className="flex-1">
                    <Settings className="w-4 h-4 mr-2" />
                    Configure
                  </Button>
                  <Button variant="tertiary" className="flex-1">
                    Sync Now
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
