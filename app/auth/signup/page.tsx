import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import Image from "next/image"

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-center gap-2 mb-4">
            <Image src="/assets/logo_wh.png" alt="SIDE Logo" width={32} height={32} />
            <span className="font-headline text-ink">SIDE</span>
          </div>
          <CardTitle className="font-card-title text-center">Create Account</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <label className="font-body-sm text-ink mb-2 block">Full Name</label>
              <Input placeholder="John Doe" />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Email</label>
              <Input type="email" placeholder="your@email.com" />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <div>
              <label className="font-body-sm text-ink mb-2 block">Confirm Password</label>
              <Input type="password" placeholder="••••••••" />
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" className="w-4 h-4" />
              <label className="font-body-sm text-ink-muted">
                I agree to the{" "}
                <Link href="/documentation" className="text-accent-blue hover:underline">
                  Terms of Service
                </Link>
              </label>
            </div>
            <Button variant="primary" className="w-full">Create Account</Button>
          </form>
          <div className="mt-6 text-center">
            <p className="font-body-sm text-ink-muted">
              Already have an account?{" "}
              <Link href="/auth/login" className="text-accent-blue hover:underline">
                Sign in
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
