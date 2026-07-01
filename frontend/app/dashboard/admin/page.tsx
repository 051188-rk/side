"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { mockUsers } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Users, Shield, FileText } from "lucide-react"

const roleVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  admin: "destructive",
  manager: "secondary",
  engineer: "default",
  viewer: "outline",
}

const permissionVariant: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  "Full Access": "destructive",
  "Limited Access": "secondary",
  "Read/Write": "default",
  "Read Only": "outline",
}

const roles = [
  { name: "Admin", permission: "Full Access", description: "Manage users, settings, and all features" },
  { name: "Manager", permission: "Limited Access", description: "Manage tickets, feedback, and analytics" },
  { name: "Engineer", permission: "Read/Write", description: "View and update assigned tickets" },
  { name: "Viewer", permission: "Read Only", description: "View-only access to dashboard" },
]

const auditLogs = [
  { timestamp: "2024-12-20 10:30:00", user: "John Doe", action: "Created Ticket", entity: "t1", details: "Created ticket for dashboard performance issue" },
  { timestamp: "2024-12-20 09:15:00", user: "Jane Smith", action: "Updated User", entity: "user_2", details: "Changed role from viewer to engineer" },
  { timestamp: "2024-12-19 16:00:00", user: "Admin User", action: "Deleted Feedback", entity: "f99", details: "Removed duplicate feedback entry" },
]

export default function AdminPage() {
  return (
    <div className="space-y-8 w-full">
      <div className="pt-2">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Admin</h1>
        <p className="text-sm text-muted-foreground mt-2">Manage users, roles, and permissions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="border border-border">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-muted-foreground" />
                <CardTitle className="text-base font-semibold">Users</CardTitle>
              </div>
              <Button size="sm" className="h-8 text-xs">Add User</Button>
            </div>
          </CardHeader>
          <CardContent className="p-0 overflow-x-auto px-6 py-4">
            <Table>
              <TableHeader>
                <TableRow className="border-t border-border">
                  <TableHead className="text-xs font-medium h-10 px-4">Name</TableHead>
                  <TableHead className="text-xs font-medium h-10 px-4">Email</TableHead>
                  <TableHead className="text-xs font-medium h-10 px-4">Role</TableHead>
                  <TableHead className="text-xs font-medium h-10 px-4">Last Active</TableHead>
                  <TableHead className="text-xs font-medium h-10 px-4"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockUsers.map((user) => (
                  <TableRow key={user.id} className="border-b border-border">
                    <TableCell className="py-3 px-4">
                      <span className="text-sm font-medium text-foreground">{user.name}</span>
                    </TableCell>
                    <TableCell className="py-3 px-4">
                      <span className="text-sm text-muted-foreground">{user.email}</span>
                    </TableCell>
                    <TableCell className="py-3 px-4">
                      <Badge variant={roleVariant[user.role] || "default"} className="text-xs capitalize">{user.role}</Badge>
                    </TableCell>
                    <TableCell className="py-3 px-4">
                      <span className="text-xs text-muted-foreground whitespace-nowrap">{formatRelativeTime(user.lastActive)}</span>
                    </TableCell>
                    <TableCell className="py-3 px-4">
                      <Button variant="ghost" size="sm" className="h-7 text-xs">Edit</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="border border-border">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-muted-foreground" />
              <CardTitle className="text-base font-semibold">Roles & Permissions</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="px-6 py-4">
            <div className="space-y-3">
              {roles.map((role) => (
                <div key={role.name} className="p-4 bg-muted rounded-md border border-border">
                  <div className="flex items-center justify-between mb-2.5">
                    <span className="text-sm font-medium text-foreground">{role.name}</span>
                    <Badge variant={permissionVariant[role.permission] || "default"} className="text-xs">{role.permission}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">{role.description}</p>
                </div>
              ))}}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border border-border">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-muted-foreground" />
            <CardTitle className="text-base font-semibold">Audit Logs</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto px-6 py-4">
          <Table>
            <TableHeader>
              <TableRow className="border-t border-border">
                <TableHead className="text-xs font-medium h-10 px-4">Timestamp</TableHead>
                <TableHead className="text-xs font-medium h-10 px-4">User</TableHead>
                <TableHead className="text-xs font-medium h-10 px-4">Action</TableHead>
                <TableHead className="text-xs font-medium h-10 px-4">Entity</TableHead>
                <TableHead className="text-xs font-medium h-10 px-4">Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {auditLogs.map((log, i) => (
                <TableRow key={i} className="border-b border-border">
                  <TableCell className="py-3 px-4">
                    <span className="text-xs text-muted-foreground whitespace-nowrap">{log.timestamp}</span>
                  </TableCell>
                  <TableCell className="py-3 px-4">
                    <span className="text-sm font-medium text-foreground">{log.user}</span>
                  </TableCell>
                  <TableCell className="py-3 px-4">
                    <span className="text-sm font-medium text-foreground">{log.action}</span>
                  </TableCell>
                  <TableCell className="py-3 px-4">
                    <span className="text-sm text-muted-foreground">{log.entity}</span>
                  </TableCell>
                  <TableCell className="py-3 px-4">
                    <span className="text-sm text-muted-foreground">{log.details}</span>
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