"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link"
import Navbar from "@/components/navbar"
import { FiMail, FiMapPin, FiSend } from "react-icons/fi"

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-canvas text-white">
      <Navbar />

      <main className="max-w-2xl mx-auto px-6 pt-32 pb-20">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">Contact Us</h1>
        <p className="text-xl text-ink-muted mb-12 leading-relaxed">Have questions? We'd love to hear from you.</p>
        
        <Card className="mb-8 bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10">
          <CardContent className="p-8">
            <form className="space-y-6">
              <div>
                <label className="text-sm font-medium text-white mb-2 block">Name</label>
                <Input placeholder="Your name" className="bg-surface-2 text-white border-hairline focus:border-accent-blue" />
              </div>
              <div>
                <label className="text-sm font-medium text-white mb-2 block">Email</label>
                <Input type="email" placeholder="your@email.com" className="bg-surface-2 text-white border-hairline focus:border-accent-blue" />
              </div>
              <div>
                <label className="text-sm font-medium text-white mb-2 block">Subject</label>
                <Input placeholder="How can we help?" className="bg-surface-2 text-white border-hairline focus:border-accent-blue" />
              </div>
              <div>
                <label className="text-sm font-medium text-white mb-2 block">Message</label>
                <textarea
                  className="w-full h-32 bg-surface-2 text-white rounded-md px-4 py-3 border border-hairline focus:outline-none focus:border-accent-blue resize-none"
                  placeholder="Tell us more..."
                />
              </div>
              <Button variant="primary" className="w-full px-8 py-4 text-base font-semibold hover:opacity-90 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                Send Message <FiSend className="w-5 h-5" />
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10 group">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-accent-blue/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <FiMail className="w-6 h-6 text-accent-blue" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Email</h3>
              <p className="text-ink-muted">support@side.ai</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-semantic-success/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-semantic-success/10 group">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-semantic-success/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <FiMapPin className="w-6 h-6 text-semantic-success" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Location</h3>
              <p className="text-ink-muted">San Francisco, CA</p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
