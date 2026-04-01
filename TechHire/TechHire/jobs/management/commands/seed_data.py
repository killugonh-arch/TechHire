"""
Management command: seed_data

Creates two test users and 15 sample job postings.

Usage:
    python manage.py seed_data

Users created:
    basic_user   / password: Pass1234!   →  Basic tier
    premium_user / password: Pass1234!   →  Premium tier
    admin        / password: admin123    →  Django superuser (Premium tier)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import UserProfile, JobPosting


JOBS = [
    {
        "title": "Senior Backend Engineer",
        "description": (
            "Design and build scalable microservices in Python/Django. "
            "You will own the architecture of our core API layer, mentor "
            "junior engineers, and collaborate closely with product. "
            "Experience with PostgreSQL, Redis, and Docker required."
        ),
        "location": "Remote",
        "company_name": "Stripe",
        "salary_range": "$180,000 – $220,000",
        "application_link": "https://stripe.com/jobs/senior-backend-engineer",
    },
    {
        "title": "Frontend Engineer (React)",
        "description": (
            "Build pixel-perfect, accessible UIs using React and TypeScript. "
            "You'll work in a small, fast-moving team shipping features weekly. "
            "Strong CSS fundamentals and a passion for performance required."
        ),
        "location": "San Francisco, CA",
        "company_name": "Linear",
        "salary_range": "$160,000 – $200,000",
        "application_link": "https://linear.app/jobs/frontend-engineer",
    },
    {
        "title": "Staff Software Engineer",
        "description": (
            "Lead cross-functional technical initiatives at the staff level. "
            "Drive architectural decisions, define engineering standards, and "
            "partner with Product and Design to ship impactful products. "
            "10+ years of industry experience preferred."
        ),
        "location": "New York, NY",
        "company_name": "Figma",
        "salary_range": "$220,000 – $280,000",
        "application_link": "https://figma.com/careers/staff-software-engineer",
    },
    {
        "title": "DevOps / Platform Engineer",
        "description": (
            "Manage our Kubernetes clusters, CI/CD pipelines, and cloud "
            "infrastructure on AWS. Improve reliability, observability, and "
            "developer experience. Terraform and Helm experience a plus."
        ),
        "location": "Remote",
        "company_name": "Vercel",
        "salary_range": "$155,000 – $190,000",
        "application_link": "https://vercel.com/careers/devops-platform-engineer",
    },
    {
        "title": "Machine Learning Engineer",
        "description": (
            "Train and deploy production ML models for ranking and recommendations. "
            "Work with large-scale data pipelines and collaborate with research "
            "scientists. Proficiency in Python, PyTorch, and MLflow expected."
        ),
        "location": "Seattle, WA",
        "company_name": "Spotify",
        "salary_range": "$190,000 – $240,000",
        "application_link": "https://spotify.com/jobs/ml-engineer",
    },
    {
        "title": "iOS Engineer",
        "description": (
            "Ship delightful native iOS features used by millions of people. "
            "Deep knowledge of Swift and UIKit required. SwiftUI and "
            "performance profiling experience are strong bonuses."
        ),
        "location": "Austin, TX",
        "company_name": "Notion",
        "salary_range": "$150,000 – $185,000",
        "application_link": "https://notion.so/careers/ios-engineer",
    },
    {
        "title": "Android Engineer",
        "description": (
            "Build and maintain our Android app in Kotlin. You'll own key "
            "features end-to-end from design review through production. "
            "Experience with Jetpack Compose and offline-first architecture is a plus."
        ),
        "location": "Remote",
        "company_name": "Duolingo",
        "salary_range": "$140,000 – $175,000",
        "application_link": "https://duolingo.com/jobs/android-engineer",
    },
    {
        "title": "Security Engineer",
        "description": (
            "Identify and remediate vulnerabilities across our product and "
            "infrastructure. Conduct threat modeling, penetration testing, "
            "and security code reviews. OSCP or equivalent certification preferred."
        ),
        "location": "Washington, DC",
        "company_name": "Cloudflare",
        "salary_range": "$170,000 – $210,000",
        "application_link": "https://cloudflare.com/careers/security-engineer",
    },
    {
        "title": "Full Stack Engineer",
        "description": (
            "Work across the entire stack — Next.js on the frontend, FastAPI "
            "on the backend — to deliver new product features. You'll be "
            "one of the first 20 engineers at a well-funded seed-stage startup."
        ),
        "location": "Remote",
        "company_name": "Loom",
        "salary_range": "$130,000 – $165,000",
        "application_link": "https://loom.com/jobs/full-stack-engineer",
    },
    {
        "title": "Data Engineer",
        "description": (
            "Build and maintain our dbt + Airflow data platform. Partner with "
            "analysts and scientists to deliver reliable, well-documented datasets. "
            "Strong SQL skills and experience with Snowflake or BigQuery required."
        ),
        "location": "Chicago, IL",
        "company_name": "Brex",
        "salary_range": "$145,000 – $180,000",
        "application_link": "https://brex.com/careers/data-engineer",
    },
    {
        "title": "Site Reliability Engineer (SRE)",
        "description": (
            "Ensure 99.99% uptime for our globally distributed platform. "
            "Write runbooks, define SLOs, and participate in on-call rotations. "
            "Strong Linux, networking, and observability (Datadog/Prometheus) skills needed."
        ),
        "location": "Remote",
        "company_name": "PlanetScale",
        "salary_range": "$160,000 – $200,000",
        "application_link": "https://planetscale.com/jobs/sre",
    },
    {
        "title": "Backend Engineer – Payments",
        "description": (
            "Build robust, compliant payment flows handling billions of dollars "
            "annually. Deep familiarity with financial systems, idempotency, "
            "and distributed transactions required. Go or Rust experience preferred."
        ),
        "location": "New York, NY",
        "company_name": "Ramp",
        "salary_range": "$175,000 – $215,000",
        "application_link": "https://ramp.com/careers/backend-payments",
    },
    {
        "title": "Developer Advocate",
        "description": (
            "Champion our developer platform through talks, blog posts, sample "
            "apps, and community engagement. You bridge Engineering and our "
            "external developer community. Public speaking and writing chops essential."
        ),
        "location": "Remote",
        "company_name": "Twilio",
        "salary_range": "$125,000 – $155,000",
        "application_link": "https://twilio.com/jobs/developer-advocate",
    },
    {
        "title": "Embedded Systems Engineer",
        "description": (
            "Write firmware in C/C++ for next-generation hardware products. "
            "Experience with RTOS, low-power design, and hardware bring-up is required. "
            "Familiarity with BLE and Wi-Fi protocols is a strong plus."
        ),
        "location": "San Jose, CA",
        "company_name": "Anker",
        "salary_range": "$135,000 – $170,000",
        "application_link": "https://anker.com/careers/embedded-systems-engineer",
    },
    {
        "title": "Engineering Manager – Platform",
        "description": (
            "Lead a team of 6 platform engineers building the foundational "
            "infrastructure that powers all product teams. You'll hire, grow, "
            "and retain top talent while staying technically engaged. "
            "Prior IC experience at senior level required."
        ),
        "location": "Remote",
        "company_name": "Retool",
        "salary_range": "$200,000 – $250,000",
        "application_link": "https://retool.com/careers/engineering-manager-platform",
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo users and job postings."

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱  Seeding TechHire database…\n")

        # ── Superuser ─────────────────────────────────────────────────────────
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@techhire.dev", "admin123")
            self.stdout.write(self.style.SUCCESS("  ✔  Created superuser: admin / admin123"))
        else:
            self.stdout.write("  –  Superuser 'admin' already exists, skipping.")

        # FIX: ensure admin always has a Premium UserProfile
        admin_user = User.objects.get(username="admin")
        UserProfile.objects.update_or_create(
            user=admin_user,
            defaults={"membership_tier": "premium"},
        )
        self.stdout.write(self.style.SUCCESS("  ✔  Ensured admin UserProfile (premium)"))

        # ── Basic user ────────────────────────────────────────────────────────
        basic_user, created = User.objects.get_or_create(username="basic_user")
        if created:
            basic_user.set_password("Pass1234!")
            basic_user.email = "basic@techhire.dev"
            basic_user.save()
            self.stdout.write(self.style.SUCCESS("  ✔  Created user: basic_user / Pass1234!"))
        UserProfile.objects.get_or_create(user=basic_user, defaults={"membership_tier": "basic"})

        # ── Premium user ──────────────────────────────────────────────────────
        premium_user, created = User.objects.get_or_create(username="premium_user")
        if created:
            premium_user.set_password("Pass1234!")
            premium_user.email = "premium@techhire.dev"
            premium_user.save()
            self.stdout.write(self.style.SUCCESS("  ✔  Created user: premium_user / Pass1234!"))
        UserProfile.objects.update_or_create(
            user=premium_user,
            defaults={"membership_tier": "premium"},
        )

        # ── Job postings ──────────────────────────────────────────────────────
        created_count = 0
        for job_data in JOBS:
            _, created = JobPosting.objects.get_or_create(
                title=job_data["title"],
                defaults=job_data,
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"  ✔  Created {created_count} job posting(s) ({len(JOBS) - created_count} already existed).")
        )
        self.stdout.write(self.style.SUCCESS("\n✅  Seed complete!\n"))
        self.stdout.write("  Login credentials:")
        self.stdout.write("    admin        / admin123   (Django admin, Premium tier)")
        self.stdout.write("    basic_user   / Pass1234!  (Basic tier)")
        self.stdout.write("    premium_user / Pass1234!  (Premium tier)\n")