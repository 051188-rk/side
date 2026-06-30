"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="items-center text-center">
          <Image src="/assets/logo_wh.png" alt="Logo" width={64} height={64} className="mb-2" />
          <CardTitle className="text-xl">Set New Password</CardTitle>
          <CardDescription>Enter your new password below</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">New Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Confirm Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <Button type="submit" className="w-full">Reset Password</Button>
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
