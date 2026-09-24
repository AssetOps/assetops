"use client";

import { useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    console.log({
      email,
      password,
    });
  }

  return (
    <main className="flex min-h-screen items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md space-y-4 rounded-xl border p-8"
      >
        <div>
          <h1 className="text-2xl font-bold">Sign in</h1>
          <p className="text-sm text-gray-500">
            Sign in to AssetTop
          </p>
        </div>

        <div>
          <label className="mb-1 block text-sm">
            Email
          </label>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-lg border p-2"
            required
          />
        </div>

        <div>
          <label className="mb-1 block text-sm">
            Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-lg border p-2"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full rounded-lg bg-black p-2 text-white"
        >
          Sign in
        </button>
      </form>
    </main>
  );
}