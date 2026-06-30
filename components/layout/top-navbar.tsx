"use client"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Bell, Search, User } from "lucide-react"

export function TopNavbar() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-background px-4">
      <div className="flex flex-1 items-center gap-4">
        <div className="relative w-full max-w-md">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search feedback, tickets, insights..."
            className="border-0 border-b border-border pl-10 focus-visible:border-ring rounded-none bg-transparent shadow-none"
          />
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="size-4" />
          <span className="absolute right-1.5 top-1.5 size-2 rounded-full bg-primary ring-2 ring-background" />
        </Button>

        <Button variant="outline" size="sm" className="gap-2">
          <Avatar className="size-5">
            <AvatarFallback className="text-[10px]">JD</AvatarFallback>
          </Avatar>
          <span className="text-xs">Profile</span>
        </Button>
      </div>
    </header>
  )
}
