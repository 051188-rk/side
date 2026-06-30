"use client"

import Link from "next/link"
import { ArrowRight, Cpu, Layers, TrendingUp, Shield, Github, Linkedin, Mail } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"

const features = [
  {
    icon: Cpu,
    title: "AI-Powered Analysis",
    description:
      "Automatically categorize, prioritize, and summarize feedback using advanced AI models. Save hours of manual work.",
    span: "md:col-span-2",
  },
  {
    icon: Layers,
    title: "Duplicate Detection",
    description:
      "Identify and group similar feedback items to reduce noise and focus on unique issues.",
    span: "",
  },
  {
    icon: TrendingUp,
    title: "Trend Analysis",
    description:
      "Get AI-generated recommendations and trend analysis to prioritize your roadmap.",
    span: "",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description:
      "Bank-grade security with SOC 2 compliance. Your data is encrypted and protected at all times.",
    span: "md:col-span-2",
  },
]

const footerLinks = {
  Product: [
    { label: "Features", href: "/about" },
    { label: "Integrations", href: "/documentation" },
    { label: "Pricing", href: "/documentation" },
    { label: "Changelog", href: "/contact" },
  ],
  Resources: [
    { label: "Documentation", href: "/documentation" },
    { label: "API Reference", href: "/documentation" },
    { label: "Blog", href: "/about" },
    { label: "Support", href: "/contact" },
  ],
  Company: [
    { label: "About", href: "/about" },
    { label: "Careers", href: "/contact" },
    { label: "Contact", href: "/contact" },
    { label: "Privacy", href: "/documentation" },
  ],
}

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <Link href="/landing">
            <img
              src="/assets/logo_wh.png"
              alt="SIDE Logo"
              width={64}
              height={64}
              className="h-16 w-16"
            />
          </Link>
          <div className="hidden items-center gap-8 md:flex">
            <Link
              href="/about"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              About
            </Link>
            <Link
              href="/documentation"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Docs
            </Link>
            <Link
              href="/contact"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Contact
            </Link>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/auth/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/auth/signup">
              <Button>
                Get Started <ArrowRight className="size-4" />
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero + Features + CTA */}
      <main className="px-4 pt-28 pb-16">
        <div className="mx-auto max-w-5xl">
          {/* Hero */}
          <div className="mb-20">
            <Badge variant="outline" className="mb-6 h-auto gap-2 px-3 py-1.5 text-xs">
              <Cpu className="size-3.5" />
              AI-Powered Feedback Intelligence
            </Badge>
            <h1 className="mb-6 text-4xl font-medium leading-tight md:text-6xl">
              Transform Feedback into Actionable Insights
            </h1>
            <p className="mb-8 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              SIDE uses advanced AI to automatically detect duplicates, categorize issues, and
              surface trends across all your feedback channels.
            </p>
            <div className="flex items-center gap-3">
              <Link href="/auth/signup">
                <Button>
                  Start Free Trial <ArrowRight className="size-4" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="ghost">Learn More</Button>
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="mb-20 grid grid-cols-1 gap-3 md:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.title} className={cn(feature.span)}>
                <CardContent className="flex items-start gap-4 px-(--card-spacing)">
                  <div className="flex size-10 shrink-0 items-center justify-center border border-border">
                    <feature.icon className="size-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <h3 className="mb-2 text-sm font-medium">{feature.title}</h3>
                    <p className="text-xs leading-relaxed text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Trusted By */}
          <div className="mb-16 text-center">
            <p className="mb-6 text-xs uppercase tracking-wider text-muted-foreground">
              Trusted by innovative teams
            </p>
            <div className="flex flex-wrap items-center justify-center gap-8">
              {["Stripe", "Vercel", "Linear", "Notion", "Figma"].map((name) => (
                <span key={name} className="text-sm text-muted-foreground">
                  {name}
                </span>
              ))}
            </div>
          </div>

          {/* CTA */}
          <Card className="text-center">
            <CardContent>
              <h2 className="mb-4 text-2xl font-medium">
                Ready to transform your feedback?
              </h2>
              <p className="mx-auto mb-6 max-w-lg text-sm text-muted-foreground">
                Join thousands of teams using SIDE to make data-driven product decisions.
              </p>
              <Link href="/auth/signup">
                <Button>
                  Start Your Free Trial <ArrowRight className="size-4" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-12">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 grid grid-cols-1 gap-8 md:grid-cols-4">
            {/* Brand */}
            <div>
              <Link href="/landing" className="mb-4 inline-block">
                <img
                  src="/assets/logo_wh.png"
                  alt="SIDE Logo"
                  width={64}
                  height={64}
                  className="h-16 w-16"
                />
              </Link>
              <p className="mb-4 text-sm text-muted-foreground">
                AI-powered customer feedback intelligence platform for modern product teams.
              </p>
              <div className="flex items-center gap-2">
                <a
                  href="#"
                  className="flex size-8 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  aria-label="GitHub"
                >
                  <Github className="size-4" />
                </a>
                <a
                  href="#"
                  className="flex size-8 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="size-4" />
                </a>
                <a
                  href="#"
                  className="flex size-8 items-center justify-center rounded-lg border border-border text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  aria-label="Email"
                >
                  <Mail className="size-4" />
                </a>
              </div>
            </div>

            {/* Link columns */}
            {Object.entries(footerLinks).map(([title, links]) => (
              <div key={title}>
                <p className="mb-4 text-sm font-medium">{title}</p>
                <ul className="space-y-2">
                  {links.map((link) => (
                    <li key={link.label}>
                      <Link
                        href={link.href}
                        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom bar */}
          <div className="flex flex-col items-center justify-between gap-4 border-t border-border pt-6 md:flex-row">
            <p className="text-sm text-muted-foreground">
              &copy; 2024 SIDE. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <Link
                href="/documentation"
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                Terms
              </Link>
              <Link
                href="/documentation"
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                Privacy
              </Link>
              <Link
                href="/contact"
                className="text-sm text-muted-foreground transition-colors hover:text-foreground"
              >
                Cookies
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
