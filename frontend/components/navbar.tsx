"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"
import Image from "next/image"
import { ArrowRight } from "lucide-react"

export default function Navbar() {
  return (
    <nav className="fixed top-6 left-1/2 z-50 flex w-auto -translate-x-1/2 items-center justify-between gap-8 rounded-full border border-border bg-background/80 px-8 py-4 shadow-2xl backdrop-blur-xl transition-all duration-300 hover:scale-105">
      <Link href="/landing" className="flex items-center gap-2 group">
        <Image
          src="/assets/logo_wh.png"
          alt="SIDE Logo"
          width={32}
          height={32}
          className="transition-transform duration-300 group-hover:rotate-12"
        />
      </Link>
      <div className="hidden items-center gap-8 md:flex">
        <Link href="/about" className="text-sm font-medium text-muted-foreground transition-colors duration-300 hover:text-foreground">
          About
        </Link>
        <Link href="/documentation" className="text-sm font-medium text-muted-foreground transition-colors duration-300 hover:text-foreground">
          Docs
        </Link>
        <Link href="/contact" className="text-sm font-medium text-muted-foreground transition-colors duration-300 hover:text-foreground">
          Contact
        </Link>
      </div>
      <div className="flex items-center gap-3">
        <Link href="/auth/login">
          <Button variant="ghost" size="sm">
            Login
          </Button>
        </Link>
        <Link href="/auth/signup">
          <Button size="sm" className="gap-2">
            Get Started <ArrowRight className="size-4" />
          </Button>
        </Link>
      </div>
    </nav>
  )
}