import React from "react";
import { Button } from "@/components/ui/button";

function Home() {
  return (
    <div className="text-center py-16">
      <h2 className="text-2xl font-semibold mb-4">
        Welcome to the Email Automation Agent
      </h2>
      <p>Streamline your email tasks with ease.</p>
      <Button className="mt-6" onClick={() => (window.location.href = "/dashboard")}>
        Get Started
      </Button>
    </div>
  );
}

export default Home;
