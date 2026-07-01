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
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Admin</h1>
        <p className="text-sm text-muted-foreground">Manage users, roles, and permissions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-muted-foreground" />
                <CardTitle>Users</CardTitle>
              </div>
              <Button>Add User</Button>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Last Active</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mockUsers.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <span className="text-sm">{user.name}</span>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm text-muted-foreground">{user.email}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={roleVariant[user.role] || "default"}>{user.role}</Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-xs text-muted-foreground">{formatRelativeTime(user.lastActive)}</span>
                    </TableCell>
                    <TableCell>
                      <Button variant="ghost">Edit</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-muted-foreground" />
              <CardTitle>Roles & Permissions</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {roles.map((role) => (
                <div key={role.name} className="p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-foreground">{role.name}</span>
                    <Badge variant={permissionVariant[role.permission] || "default"}>{role.permission}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{role.description}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-muted-foreground" />
            <CardTitle>Audit Logs</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Timestamp</TableHead>
                <TableHead>User</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Entity</TableHead>
                <TableHead>Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {auditLogs.map((log, i) => (
                <TableRow key={i}>
                  <TableCell>
                    <span className="text-xs text-muted-foreground">{log.timestamp}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{log.user}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{log.action}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-muted-foreground">{log.entity}</span>
                  </TableCell>
                  <TableCell>
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