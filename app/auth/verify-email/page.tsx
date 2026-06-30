import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <div className="flex items-center justify-center gap-2 mb-4">
            <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={32} height={32} />
            <span className="font-headline text-ink">SIDE</span>
          </div>
          <CardTitle className="font-card-title">Verify Your Email</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="font-body text-ink-muted mb-6">
            We've sent a verification link to your email address. Please check your inbox and click the link to verify your account.
          </p>
          <Button variant="primary" className="w-full mb-4">Resend Verification Email</Button>
          <div className="mt-6">
            <Link href="/auth/login" className="font-body-sm text-accent-blue hover:underline">
              Back to login
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
