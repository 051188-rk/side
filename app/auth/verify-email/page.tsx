"use client"

import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import { Mail } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="items-center text-center">
          <Image src="/assets/logo_wh.png" alt="Logo" width={64} height={64} className="mb-2" />
          <CardTitle className="text-xl">Verify Your Email</CardTitle>
          <CardDescription>
            We&apos;ve sent a verification link to your email address. Please check your inbox and click the link to verify your account.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center gap-4">
          <div className="rounded-full bg-muted p-3">
            <Mail className="h-6 w-6 text-muted-foreground" />
          </div>
          <Button className="w-full">Resend Verification Email</Button>
          <Link href="/auth/login" className="text-sm text-primary hover:underline font-medium">
            Back to login
          </Link>
        </CardContent>
      </Card>
    </div>
  )
}
