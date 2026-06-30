"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import Navbar from "@/components/navbar"
import { Target, Zap, Shield, Users } from "lucide-react"

const values = [
  {
    icon: Target,
    title: "Customer-Centric",
    description: "We believe every piece of customer feedback is valuable and deserves attention.",
  },
  {
    icon: Zap,
    title: "Data-Driven",
    description: "Decisions should be based on comprehensive analysis, not gut feelings.",
  },
  {
    icon: Shield,
    title: "Efficiency First",
    description: "AI should handle the tedious work so your team can focus on what matters.",
  },
  {
    icon: Users,
    title: "Transparency",
    description: "Clear insights and explainable AI recommendations build trust.",
  },
]

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="mx-auto max-w-4xl px-6 pt-32 pb-20">
        <h1 className="mb-6 text-5xl font-bold text-foreground md:text-6xl">About SIDE</h1>
        <p className="mb-12 text-xl leading-relaxed text-muted-foreground">
          AI-powered customer feedback intelligence for modern product teams.
        </p>

        <Card className="mb-8">
          <CardContent className="p-8">
            <p className="mb-4 text-lg leading-relaxed text-foreground">
              SIDE (Signal Desk) is an AI-powered customer feedback intelligence platform designed to help teams make
              sense of scattered feedback across multiple channels.
            </p>
            <p className="mb-4 leading-relaxed text-muted-foreground">
              Our mission is to transform how product teams collect, analyze, and act on customer feedback. By
              leveraging advanced AI, we help you identify trends, detect duplicates, and surface actionable insights
              that drive product decisions.
            </p>
            <p className="leading-relaxed text-muted-foreground">
              Founded in 2024, SIDE is built for modern product teams who want to move beyond simple feedback
              collection to intelligent feedback analysis.
            </p>
          </CardContent>
        </Card>

        <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2">
          {values.map((value) => (
            <Card key={value.title}>
              <CardContent className="p-8">
                <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-muted">
                  <value.icon className="h-7 w-7 text-foreground" />
                </div>
                <h3 className="mb-3 text-2xl font-bold text-foreground">{value.title}</h3>
                <p className="leading-relaxed text-muted-foreground">{value.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="bg-muted">
          <CardContent className="p-12 text-center">
            <h2 className="mb-4 text-3xl font-bold text-foreground">Get in Touch</h2>
            <p className="mx-auto mb-8 max-w-xl text-muted-foreground">
              Have questions or want to learn more? We&apos;d love to hear from you.
            </p>
            <Link href="/contact">
              <Button size="lg">Contact Us</Button>
            </Link>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
