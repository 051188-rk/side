"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, Key, Globe, Trash2, Copy } from "lucide-react"

export default function IntegrationsPage() {
  return (
    <div className="space-y-8 w-full">
      <div className="pt-2">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Integrations</h1>
        <p className="text-sm text-muted-foreground mt-2">Manage API keys and webhooks</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="border border-border">
          <CardHeader className="px-6 pb-4">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base font-semibold">API Keys</CardTitle>
              <Button size="sm" className="h-8 text-xs gap-2">
                <Plus className="w-3.5 h-3.5" />
                New Key
              </Button>
            </div>
          </CardHeader>
          <CardContent className="px-6 py-4">
            <div className="space-y-3">
              <div className="p-4 bg-muted rounded-lg border border-border">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-medium text-foreground">Production Key</span>
                  <Badge variant="default" className="text-xs">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs text-muted-foreground bg-secondary px-3 py-2 rounded font-mono">
                    sk_live_************************
                  </code>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <Copy className="w-3.5 h-3.5" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-3">Created: Jan 15, 2024</p>
              </div>

              <div className="p-4 bg-muted rounded-lg border border-border">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-medium text-foreground">Test Key</span>
                  <Badge variant="default" className="text-xs">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs text-muted-foreground bg-secondary px-3 py-2 rounded font-mono">
                    sk_test_************************
                  </code>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <Copy className="w-3.5 h-3.5" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-3">Created: Feb 20, 2024</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-border">
          <CardHeader className="px-6 pb-4">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base font-semibold">Webhooks</CardTitle>
              <Button size="sm" className="h-8 text-xs gap-2">
                <Plus className="w-3.5 h-3.5" />
                New Webhook
              </Button>
            </div>
          </CardHeader>
          <CardContent className="px-6 py-4">
            <div className="space-y-3">
              <div className="p-4 bg-muted rounded-lg border border-border">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-medium text-foreground">Feedback Created</span>
                  <Badge variant="default" className="text-xs">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-3">
                  <Globe className="w-3.5 h-3.5 text-muted-foreground" />
                  <code className="text-xs text-muted-foreground font-mono truncate">https://api.example.com/webhooks/feedback</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm" className="h-7 text-xs flex-1">
                    <Copy className="w-3 h-3 mr-1" />
                    Copy
                  </Button>
                  <Button variant="ghost" size="sm" className="h-7 text-xs flex-1">
                    <Trash2 className="w-3 h-3 mr-1" />
                    Delete
                  </Button>
                </div>
              </div>

              <div className="p-4 bg-muted rounded-lg border border-border">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-medium text-foreground">Ticket Updated</span>
                  <Badge variant="default" className="text-xs">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-3">
                  <Globe className="w-3.5 h-3.5 text-muted-foreground" />
                  <code className="text-xs text-muted-foreground font-mono truncate">https://api.example.com/webhooks/tickets</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm" className="h-7 text-xs flex-1">
                    <Copy className="w-3 h-3 mr-1" />
                    Copy
                  </Button>
                  <Button variant="ghost" size="sm" className="h-7 text-xs flex-1">
                    <Trash2 className="w-3 h-3 mr-1" />
                    Delete
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border border-border">
        <CardHeader className="px-6 pb-4">
          <CardTitle className="text-base font-semibold">Integration Settings</CardTitle>
        </CardHeader>
        <CardContent className="px-6 py-4">
            <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground mb-2.5 block">Webhook Secret</label>
              <Input type="password" value="whsec_************************" readOnly className="h-9 text-sm" />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground mb-2.5 block">Rate Limit (requests/minute)</label>
              <Input type="number" defaultValue={100} className="h-9 text-sm" />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground mb-2.5 block">Retry Attempts</label>
              <Input type="number" defaultValue={3} className="h-9 text-sm" />
            </div>
            <Button className="h-9 text-sm">Save Settings</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}