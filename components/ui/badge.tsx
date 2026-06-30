import { cn } from "@/lib/utils"
import { Priority, Sentiment, Status, Source } from "@/types"

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "primary" | "success" | "warning" | "error"
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center px-2 py-1 border border-border text-xs",
        {
          "bg-surface text-text-secondary": variant === "default",
          "bg-surface text-text-primary border-white": variant === "primary",
          "bg-surface text-text-primary border-white": variant === "success",
          "bg-surface text-text-primary border-white": variant === "warning",
          "bg-surface text-text-primary border-white": variant === "error",
        },
        className
      )}
      {...props}
    />
  )
}

export function PriorityBadge({ priority }: { priority: Priority }) {
  const variant = priority === "critical" ? "error" : priority === "high" ? "warning" : "default"
  return <Badge variant={variant}>{priority}</Badge>
}

export function SentimentBadge({ sentiment }: { sentiment: Sentiment }) {
  const variant = sentiment === "positive" ? "success" : sentiment === "negative" ? "error" : "default"
  return <Badge variant={variant}>{sentiment}</Badge>
}

export function StatusBadge({ status }: { status: Status }) {
  const variant = status === "resolved" ? "success" : status === "open" ? "primary" : "default"
  return <Badge variant={variant}>{status.replace("_", " ")}</Badge>
}

export function SourceBadge({ source }: { source: Source }) {
  const colors: Record<Source, string> = {
    email: "bg-blue-500/20 text-blue-400",
    discord: "bg-indigo-500/20 text-indigo-400",
    telegram: "bg-sky-500/20 text-sky-400",
    github: "bg-gray-500/20 text-gray-400",
    twitter: "bg-cyan-500/20 text-cyan-400",
    bug_form: "bg-orange-500/20 text-orange-400",
  }
  return <Badge className={colors[source]}>{source.replace("_", " ")}</Badge>
}
