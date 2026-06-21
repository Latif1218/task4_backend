"""
Database-এ Seed/Sample Data ঢোকানোর Script।
Run করার নিয়ম: python -m scripts.seed_data
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.vendor import Vendor
from app.models.category import Category
from app.models.service import Service
from app.models.order import Order
from app.models.transaction import Transaction


def seed():
    db = SessionLocal()
    try:
        # --- Admin User ---
        admin = db.query(User).filter(User.email == "admin@marketplace.com").first()
        if not admin:
            admin = User(
                full_name="Admin User",
                email="admin@marketplace.com",
                hashed_password=hash_password("Admin123!"),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            db.commit()
            print("✔ Admin User তৈরি হয়েছে: admin@marketplace.com / Admin123!")

        # --- Categories ---
        category_names = ["Home Cleaning", "Electrician", "Plumbing", "Tutoring", "Photography"]
        categories = []
        for name in category_names:
            slug = name.lower().replace(" ", "-")
            cat = db.query(Category).filter(Category.slug == slug).first()
            if not cat:
                cat = Category(name=name, slug=slug)
                db.add(cat)
                db.commit()
                print(f"✔ Category তৈরি হয়েছে: {name}")
            categories.append(cat)

        # --- Vendor User + Profile ---
        vendor_user = db.query(User).filter(User.email == "vendor@marketplace.com").first()
        if not vendor_user:
            vendor_user = User(
                full_name="Karim Vendor",
                email="vendor@marketplace.com",
                hashed_password=hash_password("Vendor123!"),
                role=UserRole.VENDOR,
            )
            db.add(vendor_user)
            db.commit()
            print("✔ Vendor User তৈরি হয়েছে: vendor@marketplace.com / Vendor123!")

        vendor_profile = db.query(Vendor).filter(Vendor.user_id == vendor_user.id).first()
        if not vendor_profile:
            vendor_profile = Vendor(
                user_id=vendor_user.id,
                business_name="Karim's Home Services",
                description="অভিজ্ঞ ও বিশ্বাসযোগ্য Home Service Provider",
                phone="01700000000",
                address="Dhaka, Bangladesh",
            )
            db.add(vendor_profile)
            db.commit()
            print("✔ Vendor Profile তৈরি হয়েছে")

        # --- Sample Services ---
        if not db.query(Service).filter(Service.vendor_id == vendor_profile.id).first():
            sample_services = [
                ("AC Repair Service", categories[1], 1500.0),
                ("House Deep Cleaning", categories[0], 2500.0),
                ("Bathroom Pipe Fitting", categories[2], 1200.0),
            ]
            for title, cat, price in sample_services:
                service = Service(
                    vendor_id=vendor_profile.id,
                    category_id=cat.id,
                    title=title,
                    description=f"{title} - Professional ও Reliable সার্ভিস",
                    price=price,
                )
                db.add(service)
            db.commit()
            print("✔ Sample Services তৈরি হয়েছে")

        # --- Normal End-User ---
        normal_user = db.query(User).filter(User.email == "user@marketplace.com").first()
        if not normal_user:
            normal_user = User(
                full_name="Rahim User",
                email="user@marketplace.com",
                hashed_password=hash_password("User123!"),
                role=UserRole.USER,
            )
            db.add(normal_user)
            db.commit()
            print("✔ End-User তৈরি হয়েছে: user@marketplace.com / User123!")

        print("\n✅ Seed Data সফলভাবে যুক্ত করা হয়েছে!")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
