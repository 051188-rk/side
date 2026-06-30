"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"
import Image from "next/image"
import { FiArrowRight } from "react-icons/fi"

export default function Navbar() {
  return (
    <nav className="fixed top-6 left-1/2 -translate-x-1/2 z-50 bg-surface-1/80 backdrop-blur-xl border border-hairline rounded-full px-8 py-4 flex items-center justify-between gap-8 shadow-2xl hover:bg-surface-1/90 transition-all duration-300 hover:scale-105">
      <Link href="/landing" className="flex items-center gap-2 group">
        <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={32} height={32} className="group-hover:rotate-12 transition-transform duration-300" />
      </Link>
      <div className="hidden md:flex items-center gap-8">
        <Link href="/about" className="text-sm font-medium text-ink-muted hover:text-white transition-colors duration-300 hover:scale-105 transform">About</Link>
        <Link href="/documentation" className="text-sm font-medium text-ink-muted hover:text-white transition-colors duration-300 hover:scale-105 transform">Docs</Link>
        <Link href="/contact" className="text-sm font-medium text-ink-muted hover:text-white transition-colors duration-300 hover:scale-105 transform">Contact</Link>
      </div>
      <div className="flex items-center gap-3">
        <Link href="/auth/login">
          <Button variant="tertiary" className="text-sm font-medium hover:bg-surface-2 transition-all duration-300 hover:scale-105">Login</Button>
        </Link>
        <Link href="/auth/signup">
          <Button variant="primary" className="text-sm font-medium hover:opacity-90 transition-all duration-300 hover:scale-105 flex items-center gap-2">
            Get Started <FiArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </div>
    </nav>
  )
}
