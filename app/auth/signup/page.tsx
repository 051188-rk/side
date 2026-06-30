"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="items-center text-center">
          <Image src="/assets/logo_wh.png" alt="Logo" width={64} height={64} className="mb-2" />
          <CardTitle className="text-xl">Create Account</CardTitle>
          <CardDescription>Get started with your free account</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Full Name</label>
              <Input placeholder="John Doe" />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Email</label>
              <Input type="email" placeholder="your@email.com" />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-foreground">Confirm Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <label className="flex items-start gap-2 text-sm text-muted-foreground cursor-pointer">
              <input type="checkbox" className="mt-0.5 h-4 w-4 rounded border-border bg-muted text-primary accent-primary" />
              <span>
                I agree to the{" "}
                <Link href="/documentation" className="text-primary hover:underline">
                  Terms of Service
                </Link>
              </span>
            </label>
            <Button type="submit" className="w-full">Create Account</Button>
          </form>
          <p className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link href="/auth/login" className="text-primary hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
