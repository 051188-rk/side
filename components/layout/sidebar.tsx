"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
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

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <>
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-surface border border-border rounded-sm text-text-primary"
      >
        <Menu className="w-4 h-4" />
      </button>
      
      <aside
        className={cn(
          "fixed left-0 top-0 h-full bg-background border-r border-border transition-all duration-300 z-40",
          collapsed ? "w-16" : "w-64",
          "lg:translate-x-0",
          "-translate-x-full lg:translate-x-0"
        )}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between p-4 border-b border-border">
            {!collapsed && (
              <Link href="/dashboard">
                <img src="/assets/logo_wh.png" alt="SIDE Logo" width={40} height={40} />
              </Link>
            )}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="hidden lg:flex p-1 hover:bg-surface rounded-sm"
            >
              {collapsed ? (
                <ChevronRight className="w-4 h-4 text-text-secondary" />
              ) : (
                <ChevronLeft className="w-4 h-4 text-text-secondary" />
              )}
            </button>
          </div>

          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = pathname?.startsWith(item.href)
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-sm transition-colors",
                    isActive
                      ? "bg-surface text-text-primary"
                      : "text-text-secondary hover:bg-surface hover:text-text-primary"
                  )}
                >
                  <item.icon className="w-4 h-4 flex-shrink-0" />
                  {!collapsed && <span className="text-xs">{item.name}</span>}
                </Link>
              )
            })}
          </nav>

          <div className="p-4 border-t border-border">
            {!collapsed && (
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 border border-border flex items-center justify-center">
                  <span className="text-xs text-text-secondary">JD</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-text-primary truncate">John Doe</p>
                  <p className="text-xs text-text-tertiary truncate">john@example.com</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </aside>
    </>
  )
}
