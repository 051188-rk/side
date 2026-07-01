"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, Key, Globe, Trash2, Copy } from "lucide-react"

export default function IntegrationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Integrations</h1>
        <p className="text-sm text-muted-foreground">Manage API keys and webhooks</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>API Keys</CardTitle>
              <Button size="sm">
                <Plus className="w-4 h-4 mr-2" />
                New Key
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground">Production Key</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs text-muted-foreground bg-secondary px-2 py-1 rounded">
                    sk_live_************************
                  </code>
                  <Button variant="ghost" size="icon-sm">
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-2">Created: Jan 15, 2024</p>
              </div>

              <div className="p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground">Test Key</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 text-xs text-muted-foreground bg-secondary px-2 py-1 rounded">
                    sk_test_************************
                  </code>
                  <Button variant="ghost" size="icon-sm">
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-2">Created: Feb 20, 2024</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Webhooks</CardTitle>
              <Button size="sm">
                <Plus className="w-4 h-4 mr-2" />
                New Webhook
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground">Feedback Created</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Globe className="w-4 h-4 text-muted-foreground" />
                  <code className="text-xs text-muted-foreground">https://api.example.com/webhooks/feedback</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm">
                    <Copy className="w-4 h-4 mr-2" />
                    Copy URL
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </Button>
                </div>
              </div>

              <div className="p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground">Ticket Updated</span>
                  <Badge variant="default">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Globe className="w-4 h-4 text-muted-foreground" />
                  <code className="text-xs text-muted-foreground">https://api.example.com/webhooks/tickets</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm">
                    <Copy className="w-4 h-4 mr-2" />
                    Copy URL
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Integration Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="text-sm text-foreground mb-2 block">Webhook Secret</label>
              <Input type="password" value="whsec_************************" readOnly />
            </div>
            <div>
              <label className="text-sm text-foreground mb-2 block">Rate Limit (requests/minute)</label>
              <Input type="number" defaultValue={100} />
            </div>
            <div>
              <label className="text-sm text-foreground mb-2 block">Retry Attempts</label>
              <Input type="number" defaultValue={3} />
            </div>
            <Button>Save Settings</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}