"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="items-center text-center">
          <Image src="/assets/logo_wh.png" alt="Logo" width={64} height={64} className="mb-2" />
          <CardTitle className="text-xl">Reset Password</CardTitle>
          <CardDescription>
            Enter your email address and we&apos;ll send you a link to reset your password.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Email</label>
              <Input type="email" placeholder="your@email.com" />
            </div>
            <Button type="submit" className="w-full">Send Reset Link</Button>
          </form>
          <p className="mt-6 text-center text-sm text-muted-foreground">
            <Link href="/auth/login" className="text-primary hover:underline font-medium">
              Back to login
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
