"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import Navbar from "@/components/navbar"
import { FiBook, FiZap, FiLayers, FiCode, FiArrowRight } from "react-icons/fi"

export default function DocumentationPage() {
  return (
    <div className="min-h-screen bg-canvas text-white">
      <Navbar />

      <main className="max-w-4xl mx-auto px-6 pt-32 pb-20">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">Documentation</h1>
        <p className="text-xl text-ink-muted mb-12 leading-relaxed">Everything you need to get started with SIDE.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-accent-blue/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiBook className="w-7 h-7 text-accent-blue" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Getting Started</h3>
              <p className="text-ink-muted mb-6 leading-relaxed">Learn how to set up your account and start collecting feedback.</p>
              <Button variant="secondary" className="w-full hover:bg-surface-3 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                Read Guide <FiArrowRight className="w-4 h-4" />
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-semantic-success/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-semantic-success/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-semantic-success/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiLayers className="w-7 h-7 text-semantic-success" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Channels Integration</h3>
              <p className="text-ink-muted mb-6 leading-relaxed">Connect your feedback sources: email, Discord, GitHub, and more.</p>
              <Button variant="secondary" className="w-full hover:bg-surface-3 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                Read Guide <FiArrowRight className="w-4 h-4" />
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-semantic-warning/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-semantic-warning/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-semantic-warning/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiZap className="w-7 h-7 text-semantic-warning" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">AI Features</h3>
              <p className="text-ink-muted mb-6 leading-relaxed">Understand how SIDE uses AI to analyze and categorize feedback.</p>
              <Button variant="secondary" className="w-full hover:bg-surface-3 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                Read Guide <FiArrowRight className="w-4 h-4" />
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-accent-blue/10 group">
            <CardContent className="p-8">
              <div className="w-14 h-14 bg-accent-blue/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <FiCode className="w-7 h-7 text-accent-blue" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">API Reference</h3>
              <p className="text-ink-muted mb-6 leading-relaxed">Complete API documentation for developers.</p>
              <Button variant="secondary" className="w-full hover:bg-surface-3 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2">
                View API <FiArrowRight className="w-4 h-4" />
              </Button>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-gradient-to-br from-surface-1 to-surface-2 border border-hairline hover:border-accent-blue/30 transition-all duration-300">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-white">Quick Links</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <Link href="#" className="block text-ink-muted hover:text-white transition-colors duration-300 hover:translate-x-2 transform inline-block">Installation Guide</Link>
              <Link href="#" className="block text-ink-muted hover:text-white transition-colors duration-300 hover:translate-x-2 transform inline-block">Configuration</Link>
              <Link href="#" className="block text-ink-muted hover:text-white transition-colors duration-300 hover:translate-x-2 transform inline-block">Best Practices</Link>
              <Link href="#" className="block text-ink-muted hover:text-white transition-colors duration-300 hover:translate-x-2 transform inline-block">Troubleshooting</Link>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
