import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-center gap-2 mb-4">
            <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={32} height={32} />
            <span className="font-headline text-ink">SIDE</span>
          </div>
          <CardTitle className="font-card-title text-center">Welcome Back</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <label className="font-body-sm text-ink mb-2 block">Email</label>
              <Input type="email" placeholder="your@email.com" />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 font-body-sm text-ink-muted">
                <input type="checkbox" className="w-4 h-4" />
                Remember me
              </label>
              <Link href="/auth/forgot-password" className="font-body-sm text-accent-blue hover:underline">
                Forgot password?
              </Link>
            </div>
            <Button variant="primary" className="w-full">Sign In</Button>
          </form>
          <div className="mt-6 text-center">
            <p className="font-body-sm text-ink-muted">
              Don't have an account?{" "}
              <Link href="/auth/signup" className="text-accent-blue hover:underline">
                Sign up
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
