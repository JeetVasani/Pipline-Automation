import httpx

async def get_user_profile(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.github.com/user", headers=headers)
        return res.json()

async def get_user_repos(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.github.com/user/repos", headers=headers)
        return res.json()

async def get_repo_issues(token: str, owner: str, repo: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        res = await client.get(url, headers=headers)
        return res.json()
