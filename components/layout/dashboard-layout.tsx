import { Sidebar } from "./sidebar"
import { TopNavbar } from "./top-navbar"

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="lg:ml-64">
        <TopNavbar />
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
