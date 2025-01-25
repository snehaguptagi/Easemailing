import React from "react";
import { Card, CardContent } from "@/components/ui/card";

function Dashboard() {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Dashboard</h2>
      <Card className="shadow mb-4">
        <CardContent>
          <p>Here you can view and manage your emails.</p>
        </CardContent>
      </Card>
    </div>
  );
}

export default Dashboard;
