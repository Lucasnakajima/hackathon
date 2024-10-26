import { Outlet, Link } from "react-router-dom";
import { Sidebar, SidebarGroup, SidebarMenu, SidebarMenuItem, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

const Layout = () => {
  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem>
            <Link to="/">Home</Link>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>
      </Sidebar>

      <main className="grid grid-cols-12 h-lvh w-full">
        <SidebarTrigger/>
        <Outlet />
      </main>

    </SidebarProvider>
  )
};

export default Layout;