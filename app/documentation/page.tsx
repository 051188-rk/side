"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import Navbar from "@/components/navbar"
import { BookOpen, Layers, Zap, Code, ArrowRight } from "lucide-react"

const sections = [
  {
    icon: BookOpen,
    title: "Getting Started",
    description: "Learn how to set up your account and start collecting feedback.",
    label: "Read Guide",
  },
  {
    icon: Layers,
    title: "Channels Integration",
    description: "Connect your feedback sources: email, Discord, GitHub, and more.",
    label: "Read Guide",
  },
  {
    icon: Zap,
    title: "AI Features",
    description: "Understand how SIDE uses AI to analyze and categorize feedback.",
    label: "Read Guide",
  },
  {
    icon: Code,
    title: "API Reference",
    description: "Complete API documentation for developers.",
    label: "View API",
  },
]

const quickLinks = ["Installation Guide", "Configuration", "Best Practices", "Troubleshooting"]

export default function DocumentationPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="mx-auto max-w-4xl px-6 pt-32 pb-20">
        <h1 className="mb-6 text-5xl font-bold text-foreground md:text-6xl">Documentation</h1>
        <p className="mb-12 text-xl leading-relaxed text-muted-foreground">
          Everything you need to get started with SIDE.
        </p>

        <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2">
          {sections.map((section) => (
            <Card key={section.title}>
              <CardContent className="p-8">
                <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-muted">
                  <section.icon className="h-7 w-7 text-foreground" />
                </div>
                <h3 className="mb-3 text-2xl font-bold text-foreground">{section.title}</h3>
                <p className="mb-6 leading-relaxed text-muted-foreground">{section.description}</p>
                <Button variant="outline" className="w-full">
                  {section.label} <ArrowRight />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-foreground">Quick Links</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {quickLinks.map((link) => (
                <Link
                  key={link}
                  href="#"
                  className="block text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link}
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
