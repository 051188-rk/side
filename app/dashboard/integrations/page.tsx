"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, Key, Globe, Trash2, Copy } from "lucide-react"

export default function IntegrationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Integrations</h1>
        <p className="font-body text-ink-muted">Manage API keys and webhooks</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="font-card-title">API Keys</CardTitle>
              <Button variant="primary" size="sm">
                <Plus className="w-4 h-4 mr-2" />
                New Key
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Production Key</span>
                  <Badge variant="success">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 font-caption text-ink-muted bg-surface-1 px-2 py-1 rounded">
                    sk_live_************************
                  </code>
                  <Button variant="tertiary" size="sm">
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <p className="font-caption text-ink-muted mt-2">Created: Jan 15, 2024</p>
              </div>

              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Test Key</span>
                  <Badge variant="success">Active</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <code className="flex-1 font-caption text-ink-muted bg-surface-1 px-2 py-1 rounded">
                    sk_test_************************
                  </code>
                  <Button variant="tertiary" size="sm">
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <p className="font-caption text-ink-muted mt-2">Created: Feb 20, 2024</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="font-card-title">Webhooks</CardTitle>
              <Button variant="primary" size="sm">
                <Plus className="w-4 h-4 mr-2" />
                New Webhook
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Feedback Created</span>
                  <Badge variant="success">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Globe className="w-4 h-4 text-ink-muted" />
                  <code className="font-caption text-ink-muted">https://api.example.com/webhooks/feedback</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="tertiary" size="sm">
                    <Copy className="w-4 h-4 mr-2" />
                    Copy URL
                  </Button>
                  <Button variant="tertiary" size="sm">
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </Button>
                </div>
              </div>

              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Ticket Updated</span>
                  <Badge variant="success">Active</Badge>
                </div>
                <div className="flex items-center gap-2 mb-2">
                  <Globe className="w-4 h-4 text-ink-muted" />
                  <code className="font-caption text-ink-muted">https://api.example.com/webhooks/tickets</code>
                </div>
                <div className="flex gap-2">
                  <Button variant="tertiary" size="sm">
                    <Copy className="w-4 h-4 mr-2" />
                    Copy URL
                  </Button>
                  <Button variant="tertiary" size="sm">
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
          <CardTitle className="font-card-title">Integration Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="font-body-sm text-ink mb-2 block">Webhook Secret</label>
              <Input type="password" value="whsec_************************" readOnly />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Rate Limit (requests/minute)</label>
              <Input type="number" defaultValue="100" />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Retry Attempts</label>
              <Input type="number" defaultValue="3" />
            </div>
            <Button variant="primary">Save Settings</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
