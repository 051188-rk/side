"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { mockChannels } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Mail, MessageSquare, Send, Github, Twitter, FileText, Zap, Settings } from "lucide-react"

const channelIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  email: Mail,
  discord: MessageSquare,
  telegram: Send,
  github: Github,
  twitter: Twitter,
  bug_form: FileText,
}

export default function ChannelsPage() {
  return (
    <div className="space-y-8 w-full">
      <div className="pt-2">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Channels</h1>
        <p className="text-sm text-muted-foreground mt-2">Manage feedback source integrations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-max">
        {mockChannels.map((channel) => {
          const Icon = channelIcons[channel.type] || Zap

          return (
            <Card key={channel.id} className="border border-border hover:shadow-md transition-shadow h-full">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-muted rounded-lg">
                    <Icon className="w-5 h-5 text-foreground" />
                  </div>
                  <Badge variant={channel.status === "connected" ? "default" : "secondary"} className="text-xs">
                    {channel.status}
                  </Badge>
                </div>
                <CardTitle className="text-base leading-snug">{channel.name}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 px-6 py-4">
                <div className="space-y-2.5 pt-2 border-t border-border">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground font-medium">Last Sync</span>
                    <span className="text-sm font-medium text-foreground">{formatRelativeTime(channel.lastSync)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-muted-foreground font-medium">Feedback Count</span>
                    <span className="text-sm font-medium text-foreground">{channel.feedbackCount}</span>
                  </div>
                </div>

                <div className="mt-4 flex gap-2 pt-2">
                  <Button variant="secondary" className="flex-1 h-8 text-xs" size="sm">
                    <Settings className="w-3.5 h-3.5 mr-1.5" />
                    Configure
                  </Button>
                  <Button variant="outline" className="flex-1 h-8 text-xs" size="sm">
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