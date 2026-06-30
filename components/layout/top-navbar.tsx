"use client"

import { Bell, Search, User } from "lucide-react"
import { Button } from "@/components/ui/button"

export function TopNavbar() {
  return (
    <header className="h-14 bg-background border-b border-border flex items-center justify-between px-4">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative max-w-md w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
          <input
            type="text"
            placeholder="Search feedback, tickets, insights..."
            className="w-full bg-surface text-text-primary text-xs pl-10 pr-4 py-2 border-b border-border focus:outline-none focus:border-white"
          />
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button className="relative p-2 hover:bg-surface rounded-sm transition-colors">
          <Bell className="w-4 h-4 text-text-secondary" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-text-secondary rounded-full" />
        </button>
        
        <Button variant="secondary" className="flex items-center gap-2">
          <User className="w-3 h-3" />
          <span className="text-xs">Profile</span>
        </Button>
      </div>
    </header>
  )
}
