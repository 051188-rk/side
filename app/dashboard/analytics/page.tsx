"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { mockAnalytics } from "@/lib/data/mock-data"
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"

const COLORS = ["#7b42bc", "#ffcf25", "#14c6cb", "#1868f2", "#00ca8e", "#e62b1e"]

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display-lg text-ink mb-2">Analytics</h1>
        <p className="font-body text-ink-muted">Track feedback trends and metrics</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="font-card-title">Sentiment Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockAnalytics.sentimentTrend}>
                <CartesianGrid strokeDasharray="3 " stroke="#3b3d45" />
                <XAxis dataKey="date" stroke="#b2b6bd" fontSize={12} />
                <YAxis stroke="#b2b6bd" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#15181e", border: "1px solid #3b3d45", borderRadius: "8px" }}
                  itemStyle={{ color: "#ffffff" }}
                />
                <Legend />
                <Line type="monotone" dataKey="positive" stroke="#00ca8e" strokeWidth={2} name="Positive" />
                <Line type="monotone" dataKey="neutral" stroke="#b2b6bd" strokeWidth={2} name="Neutral" />
                <Line type="monotone" dataKey="negative" stroke="#e62b1e" strokeWidth={2} name="Negative" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-card-title">Channel Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={mockAnalytics.channelDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name}: ${percentage}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {mockAnalytics.channelDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: "#15181e", border: "1px solid #3b3d45", borderRadius: "8px" }}
                  itemStyle={{ color: "#ffffff" }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-card-title">Feedback Volume</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockAnalytics.feedbackVolume}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3b3d45" />
                <XAxis dataKey="date" stroke="#b2b6bd" fontSize={12} />
                <YAxis stroke="#b2b6bd" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#15181e", border: "1px solid #3b3d45", borderRadius: "8px" }}
                  itemStyle={{ color: "#ffffff" }}
                />
                <Bar dataKey="count" fill="#7b42bc" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-card-title">Ticket Growth</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockAnalytics.ticketGrowth}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3b3d45" />
                <XAxis dataKey="date" stroke="#b2b6bd" fontSize={12} />
                <YAxis stroke="#b2b6bd" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#15181e", border: "1px solid #3b3d45", borderRadius: "8px" }}
                  itemStyle={{ color: "#ffffff" }}
                />
                <Legend />
                <Line type="monotone" dataKey="created" stroke="#7b42bc" strokeWidth={2} name="Created" />
                <Line type="monotone" dataKey="resolved" stroke="#00ca8e" strokeWidth={2} name="Resolved" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="font-card-title">Priority Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockAnalytics.priorityDistribution} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#3b3d45" />
              <XAxis type="number" stroke="#b2b6bd" fontSize={12} />
              <YAxis dataKey="priority" type="category" stroke="#b2b6bd" fontSize={12} width={80} />
              <Tooltip 
                contentStyle={{ backgroundColor: "#15181e", border: "1px solid #3b3d45", borderRadius: "8px" }}
                itemStyle={{ color: "#ffffff" }}
              />
              <Bar dataKey="count" fill="#14c6cb" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
