"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

type Repo = {
  id: number;
  name: string;
  html_url: string;
  description: string | null;
};

type GitHubUser = {
  login: string;
  avatar_url: string;
  name: string | null;
};

export default function Dashboard() {
  const params = useSearchParams();
  const router = useRouter();

  // username from URL OR saved session
  const urlUser = params.get("user");
  const savedUser = typeof window !== "undefined"
    ? localStorage.getItem("github_user")
    : null;

  const username = urlUser || savedUser;

  const [profile, setProfile] = useState<GitHubUser | null>(null);
  const [repos, setRepos] = useState<Repo[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Redirect if no username at all
  useEffect(() => {
    if (!username) {
      router.push("/");
    }
  }, [username]);

  // Load profile + repos
  useEffect(() => {
    if (!username) return;

    async function load() {
      try {
        const userRes = await fetch(`http://localhost:8000/me/${username}`);
        const userData = await userRes.json();

        if (!userData.profile) {
          setLoading(false);
          return;
        }

        setProfile(userData.profile);

        const reposRes = await fetch(
          `http://localhost:8000/repos/${username}`
        );
        const reposData = await reposRes.json();

        setRepos(reposData);

        // Save session if URL has user param
        if (urlUser) {
          localStorage.setItem("github_user", urlUser);
        }

      } finally {
        setLoading(false);
      }
    }

    load();
  }, [username]);

  if (loading) return <p style={{ padding: 20 }}>Loading dashboard…</p>;
  if (!profile) return <p style={{ padding: 20 }}>User not found.</p>;

  return (
    <div style={{ padding: 20, maxWidth: 900, margin: "0 auto" }}>

      {/* Profile header */}
      <div style={{ display: "flex", alignItems: "center", marginBottom: 30 }}>
        <img
          src={profile.avatar_url}
          alt="Avatar"
          style={{
            width: 80,
            height: 80,
            borderRadius: "50%",
            marginRight: 20
          }}
        />
        <div>
          <h1 style={{ margin: 0 }}>{profile.name || profile.login}</h1>
          <p style={{ margin: 0, opacity: 0.7 }}>@{profile.login}</p>
        </div>

        {/* Logout button */}
        <button
          onClick={() => {
            localStorage.removeItem("github_user");
            router.push("/");
          }}
          style={{
            marginLeft: "auto",
            padding: "8px 16px",
            border: "1px solid #ccc",
            borderRadius: 8,
            cursor: "pointer",
            background: "white"
          }}
        >
          Logout
        </button>
      </div>

      {/* Repo section */}
      <h2>Your Repositories</h2>
      <div style={{ display: "grid", gap: 15 }}>
        {repos.map((repo) => (
          <div
            key={repo.id}
            style={{
              border: "1px solid #e3e3e3",
              borderRadius: 10,
              padding: 15
            }}
          >
            <a
              href={repo.html_url}
              target="_blank"
              style={{
                fontSize: 18,
                fontWeight: "bold",
                textDecoration: "none",
                color: "#0366d6"
              }}
            >
              {repo.name}
            </a>
            <p style={{ marginTop: 5, opacity: 0.7 }}>
              {repo.description || "No description"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
