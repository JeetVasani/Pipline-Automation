"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Callback() {
  const params = useSearchParams();
  const router = useRouter();
  const code = params.get("code");

  useEffect(() => {
    if (!code) return;

    fetch(`http://localhost:8000/auth/callback?code=${code}`)
      .then(r => r.json())
      .then(data => {
        console.log("DATA:", data);
        const username = data.user.login;

        // save session
        localStorage.setItem("github_user", username);

        router.push(`/dashboard?user=${username}`);
      });
  }, [code]);

  return <p>Connecting your GitHub account…</p>;
}
