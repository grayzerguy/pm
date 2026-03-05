"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // if already logged in, go straight to board
  useEffect(() => {
    fetch("/api/board", { credentials: "include" }).then((res) => {
      if (res.ok) router.replace("/");
    });
  }, [router]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include",
    });
    if (res.ok) {
      router.replace("/");
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-[var(--surface)]">
      <form
        onSubmit={submit}
        className="w-full max-w-sm rounded-lg border border-[var(--stroke)] bg-white p-8 shadow-[var(--shadow)]"
      >
        <h1 className="mb-6 text-2xl font-semibold text-[var(--navy-dark)]">
          Sign in
        </h1>
        {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
        <div className="mb-4">
          <label className="block text-sm font-medium text-[var(--gray-text)]">
            Username
          </label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 w-full rounded-md border px-3 py-2"
            placeholder="Username"
          />
        </div>
        <div className="mb-6">
          <label className="block text-sm font-medium text-[var(--gray-text)]">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-md border px-3 py-2"
            placeholder="Password"
          />
        </div>
        <button
          type="submit"
          className="w-full rounded-md bg-[var(--primary-blue)] py-2 text-white hover:bg-[var(--accent-yellow)]"
        >
          Log in
        </button>
      </form>
    </main>
  );
}
