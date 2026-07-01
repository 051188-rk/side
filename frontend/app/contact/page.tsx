"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import Navbar from "@/components/navbar"
import { Mail, MapPin, Send } from "lucide-react"

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="mx-auto max-w-2xl px-6 pt-32 pb-20">
        <h1 className="mb-6 text-5xl font-bold text-foreground md:text-6xl">Contact Us</h1>
        <p className="mb-12 text-xl leading-relaxed text-muted-foreground">Have questions? We&apos;d love to hear from you.</p>

        <Card className="mb-8">
          <CardContent className="p-8">
            <form className="space-y-6">
              <div>
                <label className="mb-2 block text-sm font-medium text-foreground">Name</label>
                <Input placeholder="Your name" />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-foreground">Email</label>
                <Input type="email" placeholder="your@email.com" />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-foreground">Subject</label>
                <Input placeholder="How can we help?" />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-foreground">Message</label>
                <Textarea className="min-h-32" placeholder="Tell us more..." />
              </div>
              <Button type="submit" className="w-full">
                Send Message <Send />
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <Card>
            <CardContent className="p-6">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-muted">
                <Mail className="h-6 w-6 text-foreground" />
              </div>
              <h3 className="mb-2 text-xl font-bold text-foreground">Email</h3>
              <p className="text-muted-foreground">support@side.ai</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-muted">
                <MapPin className="h-6 w-6 text-foreground" />
              </div>
              <h3 className="mb-2 text-xl font-bold text-foreground">Location</h3>
              <p className="text-muted-foreground">San Francisco, CA</p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}