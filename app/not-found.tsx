import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function NotFound() {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <div className="text-center">
        <h1 className="font-display-3xl text-ink mb-4">404</h1>
        <p className="font-body-lg text-ink-muted mb-8">Page not found</p>
        <Link href="/landing">
          <Button variant="primary">Go Home</Button>
        </Link>
      </div>
    </div>
  )
}
