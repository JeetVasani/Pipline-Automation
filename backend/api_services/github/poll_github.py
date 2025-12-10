from datetime import datetime
import httpx
from db.db import SessionLocal
from api_services.email_services import send_email
from models.user_model import GitHubUser, IssueCache


async def poll_github_issues():
    db = SessionLocal()

    # get all connected GitHub users
    users = db.query(GitHubUser).all()
    if not users:
        db.close()
        return

    async with httpx.AsyncClient() as client:

        for gh_user in users:

            # fetch ALL repos for this user
            headers = {"Authorization": f"Bearer {gh_user.access_token}"}

            repos_res = await client.get(
                "https://api.github.com/user/repos",
                headers=headers
            )
            repos = repos_res.json()

            # loop over each repo
            for repo in repos:
                owner = repo["owner"]["login"]
                repo_name = repo["name"]

                issues_res = await client.get(
                    f"https://api.github.com/repos/{owner}/{repo_name}/issues",
                    headers=headers
                )
                issues = issues_res.json()

                if not isinstance(issues, list):
                    print("Skipping non-list issues:", issues)
                    continue

                for issue in issues:
                    num = issue["number"]
                    updated = datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00")).replace(tzinfo=None)


                    cache = (
                        db.query(IssueCache)
                        .filter_by(repo=repo_name, number=num)
                        .first()
                    )
                   # NEW ISSUE
                    if not cache:
                        print("NEW ISSUE RAISED")

                        title = issue["title"]
                        body_text = issue.get("body", "") or "No description"
                        repo_label = f"{owner}/{repo_name}"

                        # Defensive: GitHubUser.user may not exist
                        user_obj = gh_user.user
                        to_email = user_obj.email if user_obj else None

                        if to_email:
                            subject = f"New issue in {repo_label}: {title}"

                            html = f"""
                    <h2>New issue in {repo_label}</h2>
                    <p><strong>{title}</strong></p>
                    <p>{body_text}</p>
                    <p><a href="{issue.get('html_url')}">View on GitHub</a></p>
                    """

                            send_email(to_email, subject, html)
                            print(f"EMAIL SENT to {to_email}")
                        else:
                            print("User has no email in database. Skipping email.")

                        # Save cache
                        new_cache = IssueCache(
                            repo=repo_label,
                            number=num,
                            updated_at=updated,
                            title=title,
                            state=issue["state"],
                        )
                        db.add(new_cache)
                        db.commit()
                        continue


    db.close()