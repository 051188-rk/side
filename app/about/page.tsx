"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import Navbar from "@/components/navbar"
import { FiTarget, FiUsers, FiZap, FiShield } from "react-icons/fi"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-canvas text-white">
      <Navbar />

      <main className="max-w-4xl mx-auto px-6 pt-32 pb-20">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">About SIDE</h1>
        <p className="text-xl text-ink-muted mb-12 leading-relaxed">AI-powered customer feedback intelligence for modern product teams.</p>
        
        <Card className="mb-8 bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10">
          <CardContent className="p-8">
            <p className="text-lg text-white mb-4 leading-relaxed">
              SIDE (Signal Desk) is an AI-powered customer feedback intelligence platform designed to help teams make sense of scattered feedback across multiple channels.
            </p>
            <p className="text-ink-muted mb-4 leading-relaxed">
              Our mission is to transform how product teams collect, analyze, and act on customer feedback. By leveraging advanced AI, we help you identify trends, detect duplicates, and surface actionable insights that drive product decisions.
            </p>
            <p className="text-ink-muted leading-relaxed">
              Founded in 2024, SIDE is built for modern product teams who want to move beyond simple feedback collection to intelligent feedback analysis.
            </p>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-accent-blue/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiTarget className="w-7 h-7 text-accent-blue" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Customer-Centric</h3>
              <p className="text-ink-muted leading-relaxed">We believe every piece of customer feedback is valuable and deserves attention.</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-semantic-success/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-semantic-success/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-semantic-success/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiZap className="w-7 h-7 text-semantic-success" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Data-Driven</h3>
              <p className="text-ink-muted leading-relaxed">Decisions should be based on comprehensive analysis, not gut feelings.</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-semantic-warning/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-semantic-warning/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-semantic-warning/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiShield className="w-7 h-7 text-semantic-warning" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Efficiency First</h3>
              <p className="text-ink-muted leading-relaxed">AI should handle the tedious work so your team can focus on what matters.</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-accent-blue/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiUsers className="w-7 h-7 text-accent-blue" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Transparency</h3>
              <p className="text-ink-muted leading-relaxed">Clear insights and explainable AI recommendations build trust.</p>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-gradient-to-r from-accent-blue/20 to-semantic-success/20 border border-hairline hover:border-accent-blue/30 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
          <CardContent className="p-12 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Get in Touch</h2>
            <p className="text-ink-muted mb-8 max-w-xl mx-auto">Have questions or want to learn more? We'd love to hear from you.</p>
            <Link href="/contact">
              <Button variant="primary" className="px-8 py-4 text-base font-semibold hover:opacity-90 transition-all duration-300 hover:scale-105">Contact Us</Button>
            </Link>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
