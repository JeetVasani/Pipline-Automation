"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const saved = localStorage.getItem("github_user");
    if (saved) {
      router.push(`/dashboard?user=${saved}`);
    }
  }, []);

  const login = () => {
    const clientId = "Ov23liDEkvTDHvzQbjq4";
    const redirect = "http://localhost:3000/callback";
    const scope = "repo read:user";

    window.location.href =
      `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirect}&scope=${scope}`;
  };

  return (
    <div style={{ padding: 20 }}>
      <button onClick={login}>Login with GitHub</button>
    </div>
  );
}
