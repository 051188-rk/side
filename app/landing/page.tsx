"use client"

import Link from "next/link"
import { FiArrowRight, FiCpu, FiLayers, FiTrendingUp, FiShield, FiGithub, FiLinkedin, FiMail } from "react-icons/fi"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-text-primary">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background border-b border-border">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between h-14">
            <Link href="/landing">
              <img src="/assets/logo_wh.png" alt="SIDE Logo" width={40} height={40} />
            </Link>
            <div className="hidden md:flex items-center gap-8">
              <Link href="/about" className="text-xs text-text-secondary hover:text-text-primary transition-colors">About</Link>
              <Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Docs</Link>
              <Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Contact</Link>
            </div>
            <div className="flex items-center gap-2">
              <Link href="/auth/login">
                <button className="btn-ghost">Login</button>
              </Link>
              <Link href="/auth/signup">
                <button className="btn-primary flex items-center gap-2">
                  Get Started <FiArrowRight className="w-3 h-3" />
                </button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-28 pb-16 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="mb-20">
            <div className="inline-flex items-center gap-2 border border-border px-3 py-1 mb-6">
              <FiCpu className="w-3 h-3 text-text-secondary" />
              <span className="text-xs text-text-secondary">AI-Powered Feedback Intelligence</span>
            </div>
            <h1 className="text-4xl md:text-6xl font-medium text-text-primary mb-6 leading-tight">
              Transform Feedback into Actionable Insights
            </h1>
            <p className="text-sm text-text-secondary max-w-2xl mb-8 leading-relaxed">
              SIDE uses advanced AI to automatically detect duplicates, categorize issues, and surface trends across all your feedback channels.
            </p>
            <div className="flex items-center gap-3">
              <Link href="/auth/signup">
                <button className="btn-primary flex items-center gap-2">
                  Start Free Trial <FiArrowRight className="w-3 h-3" />
                </button>
              </Link>
              <Link href="/about">
                <button className="btn-ghost">Learn More</button>
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-20">
            <div className="md:col-span-2 card">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 border border-border flex items-center justify-center flex-shrink-0">
                  <FiCpu className="w-4 h-4 text-text-secondary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-text-primary mb-2">AI-Powered Analysis</h3>
                  <p className="text-xs text-text-secondary leading-relaxed">Automatically categorize, prioritize, and summarize feedback using advanced AI models. Save hours of manual work.</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 border border-border flex items-center justify-center flex-shrink-0">
                  <FiLayers className="w-4 h-4 text-text-secondary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-text-primary mb-2">Duplicate Detection</h3>
                  <p className="text-xs text-text-secondary leading-relaxed">Identify and group similar feedback items to reduce noise and focus on unique issues.</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 border border-border flex items-center justify-center flex-shrink-0">
                  <FiTrendingUp className="w-4 h-4 text-text-secondary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-text-primary mb-2">Trend Analysis</h3>
                  <p className="text-xs text-text-secondary leading-relaxed">Get AI-generated recommendations and trend analysis to prioritize your roadmap.</p>
                </div>
              </div>
            </div>

            <div className="md:col-span-2 card">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 border border-border flex items-center justify-center flex-shrink-0">
                  <FiShield className="w-4 h-4 text-text-secondary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-text-primary mb-2">Enterprise Security</h3>
                  <p className="text-xs text-text-secondary leading-relaxed">Bank-grade security with SOC 2 compliance. Your data is encrypted and protected at all times.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Trusted By */}
          <div className="text-center mb-16">
            <p className="text-xs text-text-secondary uppercase tracking-wider mb-6">Trusted by innovative teams</p>
            <div className="flex items-center justify-center gap-8 flex-wrap">
              <span className="text-sm text-text-secondary">Stripe</span>
              <span className="text-sm text-text-secondary">Vercel</span>
              <span className="text-sm text-text-secondary">Linear</span>
              <span className="text-sm text-text-secondary">Notion</span>
              <span className="text-sm text-text-secondary">Figma</span>
            </div>
          </div>

          {/* CTA Section */}
          <div className="card text-center">
            <h2 className="text-2xl font-medium text-text-primary mb-4">Ready to transform your feedback?</h2>
            <p className="text-xs text-text-secondary mb-6 max-w-lg mx-auto">Join thousands of teams using SIDE to make data-driven product decisions.</p>
            <Link href="/auth/signup">
              <button className="btn-primary flex items-center gap-2 mx-auto">
                Start Your Free Trial <FiArrowRight className="w-3 h-3" />
              </button>
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <Link href="/landing" className="mb-4 inline-block">
                <img src="/assets/logo_wh.png" alt="SIDE Logo" width={40} height={40} />
              </Link>
              <p className="text-xs text-text-secondary mb-4">AI-powered customer feedback intelligence platform for modern product teams.</p>
              <div className="flex items-center gap-3">
                <a href="#" className="w-8 h-8 border border-border flex items-center justify-center hover:bg-white/10 transition-colors">
                  <FiGithub className="w-3 h-3" />
                </a>
                <a href="#" className="w-8 h-8 border border-border flex items-center justify-center hover:bg-white/10 transition-colors">
                  <FiLinkedin className="w-3 h-3" />
                </a>
                <a href="#" className="w-8 h-8 border border-border flex items-center justify-center hover:bg-white/10 transition-colors">
                  <FiMail className="w-3 h-3" />
                </a>
              </div>
            </div>
            <div>
              <p className="text-xs font-medium text-text-primary mb-4">Product</p>
              <ul className="space-y-2">
                <li><Link href="/about" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Features</Link></li>
                <li><Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Integrations</Link></li>
                <li><Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Pricing</Link></li>
                <li><Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Changelog</Link></li>
              </ul>
            </div>
            <div>
              <p className="text-xs font-medium text-text-primary mb-4">Resources</p>
              <ul className="space-y-2">
                <li><Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Documentation</Link></li>
                <li><Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">API Reference</Link></li>
                <li><Link href="/about" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Support</Link></li>
              </ul>
            </div>
            <div>
              <p className="text-xs font-medium text-text-primary mb-4">Company</p>
              <ul className="space-y-2">
                <li><Link href="/about" className="text-xs text-text-secondary hover:text-text-primary transition-colors">About</Link></li>
                <li><Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Careers</Link></li>
                <li><Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Contact</Link></li>
                <li><Link href="/documentation" className="text-xs text-secondary hover:text-text-primary transition-colors">Privacy</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-xs text-text-secondary">© 2024 SIDE. All rights reserved.</p>
            <div className="flex items-center gap-4">
              <Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Terms</Link>
              <Link href="/documentation" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Privacy</Link>
              <Link href="/contact" className="text-xs text-text-secondary hover:text-text-primary transition-colors">Cookies</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
