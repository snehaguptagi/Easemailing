import React from "react";
import { Button } from "@/components/ui/button";

function Compose() {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Compose Email</h2>
      <form className="bg-white shadow p-4 rounded">
        <div className="mb-4">
          <label htmlFor="to" className="block text-sm font-medium mb-1">
            To:
          </label>
          <input
            type="email"
            id="to"
            className="w-full border p-2 rounded"
            placeholder="Recipient email"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="subject" className="block text-sm font-medium mb-1">
            Subject:
          </label>
          <input
            type="text"
            id="subject"
            className="w-full border p-2 rounded"
            placeholder="Email subject"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="body" className="block text-sm font-medium mb-1">
            Body:
          </label>
          <textarea
            id="body"
            className="w-full border p-2 rounded"
            placeholder="Email body"
          ></textarea>
        </div>
        <Button type="submit">Send Email</Button>
      </form>
    </div>
  );
}

export default Compose;
