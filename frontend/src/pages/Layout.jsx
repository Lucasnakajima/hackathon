import { Outlet, Link } from "react-router-dom";
import { Sidebar, SidebarGroup, SidebarMenu, SidebarMenuItem, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

const Layout = () => {
  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarGroup>
          <SidebarMenu>
            <SidebarMenuItem className=" h-10 font-semibold text-xl">
              <Link to="/">Minhas encomendas</Link>
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