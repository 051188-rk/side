"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  LayoutDashboard,
  MessageSquare,
  Ticket,
  GitMerge,
  Brain,
  BarChart3,
  History,
  Zap,
  Settings,
  Users,
  ChevronLeft,
  ChevronRight,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react"

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Feedback", href: "/dashboard/feedback", icon: MessageSquare },
  { name: "Tickets", href: "/dashboard/tickets", icon: Ticket },
  { name: "Clusters", href: "/dashboard/clusters", icon: GitMerge },
  { name: "AI Insights", href: "/dashboard/insights", icon: Brain },
  { name: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { name: "Memory", href: "/dashboard/memory", icon: History },
  { name: "Channels", href: "/dashboard/channels", icon: Zap },
  { name: "Integrations", href: "/dashboard/integrations", icon: Settings },
  { name: "Settings", href: "/dashboard/settings", icon: Settings },
  { name: "Admin", href: "/dashboard/admin", icon: Users },
]

function SidebarContent({ collapsed, onToggle }: { collapsed: boolean; onToggle: () => void }) {
  const pathname = usePathname()

  return (
    <div className="flex h-full flex-col">
      <div className={cn("flex items-center border-b border-border", collapsed ? "justify-center p-3" : "justify-between p-4")}>
        <Link href="/dashboard">
          <img
            src="/assets/logo_wh.png"
            alt="Logo"
            width={collapsed ? 40 : 64}
            height={collapsed ? 40 : 64}
            className="shrink-0"
          />
        </Link>
        {!collapsed && (
          <Button variant="ghost" size="icon" onClick={onToggle}>
            <PanelLeftClose className="size-4" />
          </Button>
        )}
      </div>

      <ScrollArea className="flex-1">
        <nav className={cn("grid gap-1", collapsed ? "p-2" : "p-3")}>
          {navigation.map((item) => {
            const isActive = pathname?.startsWith(item.href)
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg transition-colors",
                  collapsed ? "justify-center p-2" : "px-3 py-2",
                  isActive
                    ? "bg-muted text-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <item.icon className="size-4 shrink-0" />
                {!collapsed && <span className="text-sm">{item.name}</span>}
              </Link>
            )
          })}
        </nav>
      </ScrollArea>

      <div className={cn("border-t border-border", collapsed ? "p-3" : "p-4")}>
        <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
          <Avatar className="size-8">
            <AvatarFallback>JD</AvatarFallback>
          </Avatar>
          {!collapsed && (
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-foreground">John Doe</p>
              <p className="truncate text-xs text-muted-foreground">john@example.com</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <>
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetTrigger className="fixed left-4 top-3 z-50 lg:hidden">
          <Button variant="ghost" size="icon">
            <Menu className="size-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0">
          <SidebarContent collapsed={false} onToggle={() => {}} />
        </SheetContent>
      </Sheet>

      <aside
        className={cn(
          "fixed left-0 top-0 hidden h-full border-r border-border bg-background transition-all duration-300 lg:flex flex-col z-40",
          collapsed ? "w-16" : "w-64"
        )}
      >
        {collapsed && (
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCollapsed(false)}
            className="absolute -right-3 top-1/2 z-10 size-6 rounded-full border border-border bg-background shadow-sm"
          >
            <PanelLeftOpen className="size-3" />
          </Button>
        )}
        <SidebarContent collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
      </aside>
    </>
  )
}
