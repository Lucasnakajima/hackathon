import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <div className="grid grid-cols-12 h-lvh">
      <nav className="bg-red-300 h-full">
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/blogs">Blogs</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
        </ul>
      </nav>

      <Outlet />
    </div>
  )
};

export default Layout;