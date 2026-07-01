"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { User, Building, Palette, Bell, Shield, CreditCard } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-8 w-full">
      <div className="pt-2">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground mt-2">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <User className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Profile</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-5">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Full Name</label>
                  <Input defaultValue="John Doe" className="h-9" />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Email</label>
                  <Input defaultValue="john@example.com" type="email" className="h-9" />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Avatar URL</label>
                  <Input defaultValue="" placeholder="https://..." className="h-9" />
                </div>
                <Button className="h-9 text-sm">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <Building className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Organization</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-5">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Organization Name</label>
                  <Input defaultValue="TechCorp" className="h-9" />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Slug</label>
                  <Input defaultValue="techcorp" className="h-9" />
                </div>
                <Button className="h-9 text-sm">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <Bell className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Notifications</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-5">
                <div className="flex items-center justify-between pb-4">
                  <div>
                    <p className="text-sm font-medium text-foreground">Email Notifications</p>
                    <p className="text-xs text-muted-foreground mt-1">Receive email updates for important events</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator className="my-2" />
                <div className="flex items-center justify-between py-4">
                  <div>
                    <p className="text-sm font-medium text-foreground">Push Notifications</p>
                    <p className="text-xs text-muted-foreground mt-1">Receive push notifications in browser</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator className="my-2" />
                <div className="flex items-center justify-between pt-4">
                  <div>
                    <p className="text-sm font-medium text-foreground">Weekly Digest</p>
                    <p className="text-xs text-muted-foreground mt-1">Receive weekly summary of feedback</p>
                  </div>
                  <Switch />
                </div>
                <Button className="h-9 text-sm mt-4">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Security</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-5">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Current Password</label>
                  <Input type="password" className="h-9" />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">New Password</label>
                  <Input type="password" className="h-9" />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Confirm Password</label>
                  <Input type="password" className="h-9" />
                </div>
                <Button className="h-9 text-sm">Update Password</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <Palette className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Appearance</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-foreground mb-2.5 block">Theme</label>
                  <Select defaultValue="dark">
                    <SelectTrigger className="w-full h-9">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dark">Dark</SelectItem>
                      <SelectItem value="light">Light</SelectItem>
                      <SelectItem value="system">System</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button className="h-9 text-sm w-full">Save Changes</Button>
              </div>
            </CardContent>
          </Card>

          <Card className="border border-border">
            <CardHeader className="pb-4">
              <div className="flex items-center gap-2">
                <CreditCard className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Billing</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="px-6 py-4">
              <div className="space-y-4">
                <div className="p-4 bg-muted rounded-lg border border-border">
                  <p className="text-xs text-muted-foreground font-medium mb-1">Current Plan</p>
                  <p className="text-lg font-bold text-foreground">Pro</p>
                  <p className="text-xs text-muted-foreground mt-2.5">Renews on Jan 15, 2025</p>
                </div>
                <Button variant="secondary" className="w-full h-9 text-sm">Manage Subscription</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}