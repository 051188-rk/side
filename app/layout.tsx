import type { Metadata } from "next"
import { Plus_Jakarta_Sans } from "next/font/google"
import "./globals.css"

const plusJakartaSans = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-plus-jakarta-sans" })

export const metadata: Metadata = {
  title: "SIDE - Signal Desk | AI-Powered Customer Feedback Intelligence",
  description: "AI-powered omnichannel customer feedback intelligence platform. Collect, analyze, and prioritize customer feedback from multiple sources.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${plusJakartaSans.variable} font-sans antialiased bg-background text-text-primary`}>
        {children}
      </body>
    </html>
  )
}
