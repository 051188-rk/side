"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <div className="text-center max-w-md">
        <h1 className="font-display-3xl text-ink mb-4">500</h1>
        <p className="font-body-lg text-ink-muted mb-4">Something went wrong</p>
        <p className="font-body-sm text-ink-muted mb-8">{error.message}</p>
        <div className="flex gap-4 justify-center">
          <Button variant="primary" onClick={reset}>Try Again</Button>
          <Link href="/landing">
            <Button variant="secondary">Go Home</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
