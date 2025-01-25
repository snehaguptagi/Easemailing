import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="bg-blue-500 text-white py-4 shadow">
      <nav className="container mx-auto flex justify-between">
        <h1 className="text-xl font-bold">Email Automation Agent</h1>
        <div>
          <Link to="/" className="mr-4 hover:underline">
            Home
          </Link>
          <Link to="/dashboard" className="mr-4 hover:underline">
            Dashboard
          </Link>
          <Link to="/compose" className="hover:underline">
            Compose
          </Link>
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
