import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-center gap-2 mb-4">
            <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={32} height={32} />
            <span className="font-headline text-ink">SIDE</span>
          </div>
          <CardTitle className="font-card-title text-center">Reset Password</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="font-body text-ink-muted mb-6">
            Enter your email address and we'll send you a link to reset your password.
          </p>
          <form className="space-y-4">
            <div>
              <label className="font-body-sm text-ink mb-2 block">Email</label>
              <Input type="email" placeholder="your@email.com" />
            </div>
            <Button variant="primary" className="w-full">Send Reset Link</Button>
          </form>
          <div className="mt-6 text-center">
            <Link href="/auth/login" className="font-body-sm text-accent-blue hover:underline">
              Back to login
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
