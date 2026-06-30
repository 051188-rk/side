"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table"
import { mockUsers } from "@/lib/data/mock-data"
import { formatRelativeTime } from "@/lib/utils"
import { Users, Shield, FileText } from "lucide-react"

export default function AdminPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Admin</h1>
        <p className="font-body text-ink-muted">Manage users, roles, and permissions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-ink-muted" />
                <CardTitle className="font-card-title">Users</CardTitle>
              </div>
              <Button variant="primary">
                Add User
              </Button>
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
                      <span className="font-body-sm">{user.name}</span>
                    </TableCell>
                    <TableCell>
                      <span className="font-body-sm text-ink-muted">{user.email}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={user.role === "admin" ? "error" : "default"}>{user.role}</Badge>
                    </TableCell>
                    <TableCell>
                      <span className="font-caption text-ink-muted">{formatRelativeTime(user.lastActive)}</span>
                    </TableCell>
                    <TableCell>
                      <Button variant="tertiary">Edit</Button>
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
              <Shield className="w-5 h-5 text-ink-muted" />
              <CardTitle className="font-card-title">Roles & Permissions</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Admin</span>
                  <Badge variant="error">Full Access</Badge>
                </div>
                <p className="font-caption text-ink-muted">Manage users, settings, and all features</p>
              </div>
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Manager</span>
                  <Badge variant="warning">Limited Access</Badge>
                </div>
                <p className="font-caption text-ink-muted">Manage tickets, feedback, and analytics</p>
              </div>
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Engineer</span>
                  <Badge variant="default">Read/Write</Badge>
                </div>
                <p className="font-caption text-ink-muted">View and update assigned tickets</p>
              </div>
              <div className="p-4 bg-surface-2 rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-body-sm text-ink">Viewer</span>
                  <Badge variant="default">Read Only</Badge>
                </div>
                <p className="font-caption text-ink-muted">View-only access to dashboard</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-ink-muted" />
            <CardTitle className="font-card-title">Audit Logs</CardTitle>
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
              <TableRow>
                <TableCell>
                  <span className="font-caption text-ink-muted">2024-12-20 10:30:00</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">John Doe</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">Created Ticket</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">t1</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">Created ticket for dashboard performance issue</span>
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <span className="font-caption text-ink-muted">2024-12-20 09:15:00</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">Jane Smith</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">Updated User</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">user_2</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">Changed role from viewer to engineer</span>
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <span className="font-caption text-ink-muted">2024-12-19 16:00:00</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">Admin User</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm">Deleted Feedback</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">f99</span>
                </TableCell>
                <TableCell>
                  <span className="font-body-sm text-ink-muted">Removed duplicate feedback entry</span>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
