"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { User, Building, Palette, Bell, Shield, CreditCard } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Settings</h1>
        <p className="font-body text-ink-muted">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <User className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Profile</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Full Name</label>
                  <Input defaultValue="John Doe" />
                </div>
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Email</label>
                  <Input defaultValue="john@example.com" type="email" />
                </div>
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Avatar URL</label>
                  <Input defaultValue="" placeholder="https://..." />
                </div>
                <Button variant="primary">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Building className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Organization</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Organization Name</label>
                  <Input defaultValue="TechCorp" />
                </div>
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Slug</label>
                  <Input defaultValue="techcorp" />
                </div>
                <Button variant="primary">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Bell className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Notifications</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-body-sm text-ink">Email Notifications</p>
                    <p className="font-caption text-ink-muted">Receive email updates for important events</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-body-sm text-ink">Push Notifications</p>
                    <p className="font-caption text-ink-muted">Receive push notifications in browser</p>
                  </div>
                  <input type="checkbox" defaultChecked className="w-5 h-5" />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-body-sm text-ink">Weekly Digest</p>
                    <p className="font-caption text-ink-muted">Receive weekly summary of feedback</p>
                  </div>
                  <input type="checkbox" className="w-5 h-5" />
                </div>
                <Button variant="primary">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Security</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Current Password</label>
                  <Input type="password" />
                </div>
                <div>
                  <label className="font-body-sm text-ink mb-2 block">New Password</label>
                  <Input type="password" />
                </div>
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Confirm Password</label>
                  <Input type="password" />
                </div>
                <Button variant="primary">Update Password</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Palette className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Appearance</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="font-body-sm text-ink mb-2 block">Theme</label>
                  <select className="input-field w-full">
                    <option>Dark</option>
                    <option>Light</option>
                    <option>System</option>
                  </select>
                </div>
                <Button variant="primary">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <CreditCard className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Billing</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-surface-2 rounded-md">
                  <p className="font-body-sm text-ink mb-1">Current Plan</p>
                  <p className="font-headline text-ink">Pro</p>
                  <p className="font-caption text-ink-muted mt-2">Renews on Jan 15, 2025</p>
                </div>
                <Button variant="secondary" className="w-full">Manage Subscription</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
