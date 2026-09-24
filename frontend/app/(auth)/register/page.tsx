"use client";

import { useState } from "react";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    console.log({
      emailProvided: email.length > 0,
      passwordProvided: password.length > 0,
    });
  }

  return (
    <main className="flex min-h-screen items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md space-y-4 rounded-xl border p-8"
      >
        <div>
          <h1 className="text-2xl font-bold">Create account</h1>
          <p className="text-sm text-gray-500">Create your AssetTop account</p>
        </div>

        <div>
          <label htmlFor="email" className="mb-1 block text-sm">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full rounded-lg border p-2"
            required
          />
        </div>

        <div>
          <label htmlFor="password" className="mb-1 block text-sm">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full rounded-lg border p-2"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full rounded-lg bg-black p-2 text-white"
        >
          Create account
        </button>
      </form>
    </main>
  );
}
