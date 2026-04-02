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
        "title": "Senior Software Engineer",
        "description": "Build and maintain web applications using Python/Django. PRC license and experience with PostgreSQL and Docker required.",
        "location": "Makati, Metro Manila",
        "company_name": "Ayala Corporation",
        "salary_range": "₱80,000 – ₱120,000",
        "application_link": "https://careers.ayala.com/senior-software-engineer",
    },
    {
        "title": "Registered Nurse",
        "description": "Provide direct patient care including assessment and medication administration. PRC license and BLS certification required.",
        "location": "Cebu City, Cebu",
        "company_name": "Chong Hua Hospital",
        "salary_range": "₱25,000 – ₱40,000",
        "application_link": "https://chonghua.com.ph/careers/registered-nurse",
    },
    {
        "title": "General Physician",
        "description": "Conduct medical consultations and prescribe treatments for outpatient and inpatient cases. PRC license with 2 years experience required.",
        "location": "Tacloban, Leyte",
        "company_name": "Eastern Visayas Regional Medical Center",
        "salary_range": "₱60,000 – ₱90,000",
        "application_link": "https://evrmc.doh.gov.ph/careers/general-physician",
    },
    {
        "title": "Civil Engineer",
        "description": "Oversee construction projects and conduct site inspections. PRC license and AutoCAD experience required.",
        "location": "Davao City, Davao del Sur",
        "company_name": "DMCI Holdings",
        "salary_range": "₱35,000 – ₱60,000",
        "application_link": "https://dmci.com.ph/jobs/civil-engineer",
    },
    {
        "title": "High School Teacher (Mathematics)",
        "description": "Teach Math to Junior and Senior High School students under the DepEd K–12 curriculum. LET passer required.",
        "location": "Quezon City, Metro Manila",
        "company_name": "Ateneo de Manila University",
        "salary_range": "₱22,000 – ₱35,000",
        "application_link": "https://ateneo.edu/careers/hs-teacher-math",
    },
    {
        "title": "Accountant",
        "description": "Manage financial records and prepare BIR tax reports. CPA license and experience with QuickBooks or SAP preferred.",
        "location": "Pasig, Metro Manila",
        "company_name": "SM Investments Corporation",
        "salary_range": "₱30,000 – ₱55,000",
        "application_link": "https://sminvestments.com/careers/accountant",
    },
    {
        "title": "Electrical Engineer",
        "description": "Design and maintain electrical systems for commercial facilities. PRC license required; AutoCAD Electrical experience is a plus.",
        "location": "Iloilo City, Iloilo",
        "company_name": "Aboitiz Power Corporation",
        "salary_range": "₱35,000 – ₱65,000",
        "application_link": "https://aboitizpower.com/careers/electrical-engineer",
    },
    {
        "title": "Physical Therapist",
        "description": "Provide rehabilitation services and develop treatment plans for patients. Valid PRC license required.",
        "location": "Bacolod, Negros Occidental",
        "company_name": "Corazon Locsin Montelibano Memorial Regional Hospital",
        "salary_range": "₱22,000 – ₱35,000",
        "application_link": "https://clmmrh.doh.gov.ph/careers/physical-therapist",
    },
    {
        "title": "Call Center Agent (Customer Service)",
        "description": "Handle inbound and outbound calls for international clients. Strong English communication skills required. Fresh graduates welcome.",
        "location": "Pasay, Metro Manila",
        "company_name": "Concentrix Philippines",
        "salary_range": "₱18,000 – ₱28,000",
        "application_link": "https://concentrix.com/ph/careers/call-center-agent",
    },
    {
        "title": "Agricultural Technician",
        "description": "Assist farmers with modern techniques and conduct field visits for pest control and soil management guidance.",
        "location": "Cabanatuan, Nueva Ecija",
        "company_name": "Department of Agriculture – Region III",
        "salary_range": "₱18,000 – ₱28,000",
        "application_link": "https://da.gov.ph/careers/agricultural-technician",
    },
    {
        "title": "Pharmacist",
        "description": "Dispense medications and ensure compliance with PDEA and FDA regulations. PRC license required.",
        "location": "Cagayan de Oro, Misamis Oriental",
        "company_name": "Mercury Drug Corporation",
        "salary_range": "₱28,000 – ₱45,000",
        "application_link": "https://mercurydrug.com/careers/pharmacist",
    },
    {
        "title": "Architect",
        "description": "Prepare architectural designs for residential and commercial projects. PRC license and Revit or SketchUp skills required.",
        "location": "Taguig, Metro Manila",
        "company_name": "Rockwell Land Corporation",
        "salary_range": "₱40,000 – ₱75,000",
        "application_link": "https://rockwellland.com.ph/careers/architect",
    },
    {
        "title": "Social Worker",
        "description": "Provide casework services to vulnerable individuals and families. Conduct home visits and coordinate with LGUs. RSW license required.",
        "location": "Zamboanga City, Zamboanga del Sur",
        "company_name": "Department of Social Welfare and Development",
        "salary_range": "₱20,000 – ₱33,000",
        "application_link": "https://dswd.gov.ph/careers/social-worker",
    },
    {
        "title": "Mechanical Engineer",
        "description": "Install and maintain mechanical systems including HVAC and production machinery. PRC license required.",
        "location": "Laguna, Calabarzon",
        "company_name": "Toyota Motor Philippines",
        "salary_range": "₱35,000 – ₱65,000",
        "application_link": "https://toyota.com.ph/careers/mechanical-engineer",
    },
    {
        "title": "Hotel Front Desk Officer",
        "description": "Assist guests with check-in, check-out, and reservations. HRM or Tourism degree preferred.",
        "location": "Boracay, Aklan",
        "company_name": "Shangri-La Boracay Resort",
        "salary_range": "₱18,000 – ₱28,000",
        "application_link": "https://shangri-la.com/boracay/careers/front-desk-officer",
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
