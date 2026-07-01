"use client"

import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"
import { 
  FiHome, 
  FiMessageSquare, 
  FiZap, 
  FiLayers, 
  FiBarChart2, 
  FiGrid, 
  FiSettings, 
  FiKey, 
  FiDatabase,
  FiUsers,
  FiLogOut
} from "react-icons/fi"
import { cn } from "@/lib/utils"

const navItems = [
  { href: "/dashboard", icon: FiHome, label: "Overview" },
  { href: "/dashboard/feedback", icon: FiMessageSquare, label: "Feedback" },
  { href: "/dashboard/insights", icon: FiZap, label: "Insights" },
  { href: "/dashboard/tickets", icon: FiLayers, label: "Tickets" },
  { href: "/dashboard/clusters", icon: FiGrid, label: "Clusters" },
  { href: "/dashboard/analytics", icon: FiBarChart2, label: "Analytics" },
  { href: "/dashboard/channels", icon: FiGrid, label: "Channels" },
  { href: "/dashboard/memory", icon: FiDatabase, label: "Memory" },
  { href: "/dashboard/integrations", icon: FiKey, label: "Integrations" },
  { href: "/dashboard/settings", icon: FiSettings, label: "Settings" },
  { href: "/dashboard/admin", icon: FiUsers, label: "Admin" },
]

export default function DashboardSidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-surface-1 border-r border-hairline flex flex-col z-40">
      {/* Logo */}
      <div className="p-6 border-b border-hairline">
        <Link href="/dashboard" className="flex items-center gap-3 group">
          <div className="relative">
            <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={40} height={40} className="group-hover:rotate-12 transition-transform duration-300" />
          </div>
          <span className="text-xl font-bold text-white group-hover:text-accent-blue transition-colors duration-300">SIDE</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          const Icon = item.icon
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group",
                isActive
                  ? "bg-accent-blue/20 text-accent-blue border border-accent-blue/30"
                  : "text-ink-muted hover:text-white hover:bg-surface-2 border border-transparent"
              )}
            >
              <Icon className={cn(
                "w-5 h-5 transition-transform duration-300",
                isActive ? "scale-110" : "group-hover:scale-110"
              )} />
              <span className="font-medium">{item.label}</span>
              {isActive && (
                <div className="ml-auto w-2 h-2 bg-accent-blue rounded-full animate-pulse" />
              )}
            </Link>
          )
        })}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-hairline">
        <Link
          href="/auth/login"
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-ink-muted hover:text-white hover:bg-surface-2 transition-all duration-300 group"
        >
          <FiLogOut className="w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
          <span className="font-medium">Logout</span>
        </Link>
      </div>
    </aside>
  )
}