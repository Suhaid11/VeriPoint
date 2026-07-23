"""
VeriPoint — Management Command: seed_data

Populates the SQLite3 database with authentic Indian business listings (2+ per category),
at least 5 detailed evidence-backed reviews per business (60+ total reviews),
verified documents, community interactions, and computed trust scores.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import random

from apps.accounts.models import User, UserProfile, Reputation
from apps.businesses.models import Category, Business, BusinessPhoto
from apps.reviews.models import Review, Evidence, TrustScore, EvidenceVerification
from apps.reviews.scoring import calculate_trust_score
from apps.community.models import Comment, Vote, BusinessResponse, Bookmark
from apps.notifications.models import Notification
from apps.moderation.models import AuditLog


class Command(BaseCommand):
    help = 'Populates the database with authentic Indian business listings and minimum 5 reviews per business.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Cleaning up existing data & re-seeding with min 5 reviews per business...'))

        with transaction.atomic():
            # Clear old records
            AuditLog.objects.all().delete()
            Notification.objects.all().delete()
            Bookmark.objects.all().delete()
            BusinessResponse.objects.all().delete()
            Vote.objects.all().delete()
            Comment.objects.all().delete()
            EvidenceVerification.objects.all().delete()
            TrustScore.objects.all().delete()
            Evidence.objects.all().delete()
            Review.objects.all().delete()
            BusinessPhoto.objects.all().delete()
            Business.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

            self._create_categories()
            self._create_users()
            self._create_businesses()
            self._create_reviews_and_evidence()
            self._create_community_interactions()

        self.stdout.write(self.style.SUCCESS('Successfully seeded database! Every business now has at least 5 evidence-backed reviews.'))

    def _create_categories(self):
        self.stdout.write('  -> Creating 6 clean categories...')
        categories_data = [
            {'name': 'Healthcare & Hospitals', 'icon': 'activity', 'desc': 'Multispecialty hospitals, diagnostic centers, and super-specialty clinics'},
            {'name': 'Restaurants & Fine Dining', 'icon': 'utensils', 'desc': 'Heritage tiffin rooms, fine dining establishments, and iconic culinary hubs'},
            {'name': 'Electronics & Retail', 'icon': 'laptop', 'desc': 'Consumer electronics mega-stores, appliance outlets, and digital retail chains'},
            {'name': 'Automotive & Dealerships', 'icon': 'car', 'desc': 'Authorized auto dealerships, multi-brand service centers, and OEM repairs'},
            {'name': 'Software & Enterprise Tech', 'icon': 'code', 'desc': 'SaaS platforms, cloud infrastructure providers, and software consultancies'},
            {'name': 'Finance & Real Estate', 'icon': 'landmark', 'desc': 'Banking institutions, real estate developers, and financial services'},
        ]

        self.categories = []
        for idx, cat_info in enumerate(categories_data):
            cat = Category.objects.create(
                name=cat_info['name'],
                icon=cat_info['icon'],
                description=cat_info['desc'],
                display_order=idx + 1,
                is_active=True
            )
            self.categories.append(cat)

    def _create_users(self):
        self.stdout.write('  -> Creating Indian user accounts...')

        # Admin User
        self.admin_user = User.objects.filter(username='admin').first()
        if not self.admin_user:
            self.admin_user = User.objects.create(
                username='admin',
                email='admin@veripoint.in',
                first_name='Rajesh',
                last_name='Kumar',
                role=User.Role.ADMIN,
                is_staff=True,
                is_superuser=True,
            )
            self.admin_user.set_password('admin123')
            self.admin_user.save()

        # Business Owners
        self.owners = []
        owner_names = [
            ('dr_sangita_apollo', 'Dr. Sangita', 'Reddy', 'sangita@apollohospitals.com'),
            ('dr_ranjan_manipal', 'Dr. Ranjan', 'Pai', 'ranjan@manipalhospitals.com'),
            ('hemamalini_mtr', 'Hemamalini', 'Maiya', 'hema@mavallitiffinroom.com'),
            ('sumesh_paragon', 'Sumesh', 'Paragon', 'sumesh@paragonrestaurant.in'),
            ('avijit_croma', 'Avijit', 'Mitra', 'avijit@croma.com'),
            ('mukesh_reliance', 'Mukesh', 'Ambani', 'contact@reliancedigital.in'),
            ('ashok_mandovi', 'Ashok', 'Shet', 'ashok@mandovi.in'),
            ('tarun_popular', 'Tarun', 'Popular', 'tarun@popularvhes.com'),
            ('sridhar_zoho', 'Sridhar', 'Vembu', 'sridhar@zohocorp.com'),
            ('girish_freshworks', 'Girish', 'Mathrubootham', 'girish@freshworks.com'),
            ('sashi_hdfc', 'Sashidhar', 'Jagdishan', 'sashi@hdfcbank.com'),
            ('irfan_prestige', 'Irfan', 'Razack', 'irfan@prestigeconstructions.com'),
        ]
        for username, fname, lname, email in owner_names:
            u = User.objects.create(
                username=username,
                email=email,
                first_name=fname,
                last_name=lname,
                role=User.Role.BUSINESS_OWNER,
            )
            u.set_password('password123')
            u.save()
            self.owners.append(u)

        # Reviewers (14 Diverse Indian Reviewers)
        self.reviewers = []
        reviewer_names = [
            ('ananya_sharma', 'Ananya', 'Sharma', 'ananya.s@gmail.com'),
            ('karthik_rajan', 'Karthik', 'Rajan', 'karthik.r@outlook.com'),
            ('priya_nair', 'Priya', 'Nair', 'priya.nair@yahoo.co.in'),
            ('rahul_verma', 'Rahul', 'Verma', 'rahul.v@gmail.com'),
            ('vikram_aditya', 'Vikram', 'Aditya', 'vikram.a@rediffmail.com'),
            ('sneha_patel', 'Sneha', 'Patel', 'sneha.p@gmail.com'),
            ('arjun_mehta', 'Arjun', 'Mehta', 'arjun.m@gmail.com'),
            ('divya_krishnan', 'Divya', 'Krishnan', 'divya.k@gmail.com'),
            ('rohan_gupta', 'Rohan', 'Gupta', 'rohan.g@gmail.com'),
            ('meera_iyer', 'Meera', 'Iyer', 'meera.i@gmail.com'),
            ('amit_das', 'Amit', 'Das', 'amit.d@gmail.com'),
            ('pooja_joshi', 'Pooja', 'Joshi', 'pooja.j@gmail.com'),
            ('siddharth_menon', 'Siddharth', 'Menon', 'siddharth.m@gmail.com'),
            ('ritu_saxena', 'Ritu', 'Saxena', 'ritu.s@gmail.com'),
        ]
        for username, fname, lname, email in reviewer_names:
            u = User.objects.create(
                username=username,
                email=email,
                first_name=fname,
                last_name=lname,
                role=User.Role.REVIEWER,
            )
            u.set_password('password123')
            u.save()
            self.reviewers.append(u)

    def _create_businesses(self):
        self.stdout.write('  -> Creating 12 Indian businesses (2 per category)...')
        businesses_data = [
            # Category 0: Healthcare (2)
            {
                'name': 'Apollo Hospital Bannerghatta',
                'category': self.categories[0],
                'owner': self.owners[0],
                'short_description': 'JCI-accredited 250-bed super specialty hospital opposite IIM Bangalore.',
                'description': 'Apollo Hospital Bannerghatta features 24/7 emergency trauma care, advanced MRI/CT diagnostic labs, cardiac catheterization, and transparent cashless billing desk.',
                'address': '154/11, Opp. IIM, Bannerghatta Road',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560076',
                'phone': '+91 80 2630 4050',
                'email': 'contact@apollohospitalsbangalore.com',
                'website': 'https://apollohospitalsbangalore.com',
                'is_verified': True,
            },
            {
                'name': 'Manipal Hospital Old Airport Road',
                'category': self.categories[0],
                'owner': self.owners[1],
                'short_description': 'Multi-specialty flagship hospital known for oncology, cardiology, and organ transplants.',
                'description': 'Manipal Hospital is a premier quaternary care hospital providing comprehensive diagnostic imaging, robotic surgery, and dedicated international patient care desk.',
                'address': '98, HAL Old Airport Road, Kodihalli',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560017',
                'phone': '+91 80 2502 4444',
                'email': 'info@manipalhospitals.com',
                'website': 'https://manipalhospitals.com',
                'is_verified': True,
            },

            # Category 1: Dining (2)
            {
                'name': 'Mavalli Tiffin Room (MTR Original)',
                'category': self.categories[1],
                'owner': self.owners[2],
                'short_description': 'Heritage South Indian breakfast establishment founded in 1924.',
                'description': 'The original MTR near Lalbagh Main Road, famous for inventing the Rava Idli, serving pure ghee Masala Dosa, Chandrahara, and traditional South Indian Filter Coffee.',
                'address': '14, Lalbagh Main Road, Sudhama Nagar',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560027',
                'phone': '+91 80 2222 0022',
                'email': 'info@mavallitiffinroom.com',
                'website': 'https://mavallitiffinroom.com',
                'is_verified': True,
            },
            {
                'name': 'Paragon Restaurant & Catering',
                'category': self.categories[1],
                'owner': self.owners[3],
                'short_description': 'Legendary Malabar culinary destination world-famous for Biryani and Seafood.',
                'description': 'Paragon is a celebrated heritage dining icon in Kozhikode, renowned for Malabar Mutton Biryani, Fish Moilee, and authentic Kerala seafood delicacies.',
                'address': 'Kannur Road, Near Head Post Office',
                'city': 'Kozhikode',
                'state': 'Kerala',
                'zip_code': '673001',
                'phone': '+91 495 276 8920',
                'email': 'info@paragonrestaurant.in',
                'website': 'https://paragonrestaurant.in',
                'is_verified': True,
            },

            # Category 2: Electronics (2)
            {
                'name': 'Croma Electronics Koramangala',
                'category': self.categories[2],
                'owner': self.owners[4],
                'short_description': 'Tata-backed mega electronics store for laptops, smartphones, and appliances.',
                'description': 'Located at Indraprastha Equinox on 100ft Inner Ring Road, Koramangala. Features interactive demo zones, official brand warranties, transparent GST billing, and live testing.',
                'address': 'Indraprastha Equinox, 100 Feet Inner Ring Road, Koramangala',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560095',
                'phone': '+91 77958 38018',
                'email': 'support@croma.com',
                'website': 'https://croma.com',
                'is_verified': True,
            },
            {
                'name': 'Reliance Digital Phoenix Marketcity',
                'category': self.categories[2],
                'owner': self.owners[5],
                'short_description': 'India’s largest electronics retail chain featuring audio, IT, and home appliances.',
                'description': 'Reliance Digital at Phoenix Marketcity Lower Parel features ResQ tech service support, comprehensive device warranty plans, and live audio testing rooms.',
                'address': 'Lower Ground Floor, Phoenix Marketcity, Lower Parel',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'zip_code': '400013',
                'phone': '+91 22 4001 0000',
                'email': 'reliancedigital@ril.com',
                'website': 'https://reliancedigital.in',
                'is_verified': True,
            },

            # Category 3: Automotive (2)
            {
                'name': 'Mandovi Motors Maruti Suzuki Arena',
                'category': self.categories[3],
                'owner': self.owners[6],
                'short_description': 'Authorized Maruti Suzuki sales and certified service center.',
                'description': 'Mandovi Motors in Basaveshwara Nagar provides authorized Maruti Suzuki vehicle servicing, original MGP spare parts replacement, automated wheel alignment, and video inspection reports.',
                'address': '113/2-1, 4th Stage, West of Chord Road, Basaveshwara Nagar',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560079',
                'phone': '+91 98860 03030',
                'email': 'connect@mandovi.in',
                'website': 'https://mandovi.in',
                'is_verified': True,
            },
            {
                'name': 'Popular Vehicles & Services Tata Motors',
                'category': self.categories[3],
                'owner': self.owners[7],
                'short_description': 'Premier Tata Motors passenger vehicle dealership & EV service hub.',
                'description': 'Popular Vehicles is one of South India’s largest automotive dealer networks, providing Tata EV fast charging hubs, body repairs, and digital service estimates.',
                'address': 'NH 44, Edappally Toll, Cochin',
                'city': 'Kochi',
                'state': 'Kerala',
                'zip_code': '682024',
                'phone': '+91 484 280 6000',
                'email': 'sales@popularvhes.com',
                'website': 'https://popularmaruti.com',
                'is_verified': True,
            },

            # Category 4: Software (2)
            {
                'name': 'Zoho Corporation',
                'category': self.categories[4],
                'owner': self.owners[8],
                'short_description': 'Global cloud software suite developer for business CRM, books, and workspace tools.',
                'description': 'Zoho Corporation builds privacy-first business software trusted by 100M+ global users. Headquartered at Estancia IT Park near Chennai.',
                'address': 'Estancia IT Park, Plot No. 6, GST Road, Vallancheri',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'zip_code': '603202',
                'phone': '+91 44 6744 7070',
                'email': 'sales@zohocorp.com',
                'website': 'https://zoho.com',
                'is_verified': True,
            },
            {
                'name': 'Freshworks Global HQ',
                'category': self.categories[4],
                'owner': self.owners[9],
                'short_description': 'AI-powered customer service and IT service management (ITSM) SaaS platform.',
                'description': 'Freshworks makes business software including Freshdesk and Freshservice that empowers customer support and IT teams across 60,000+ businesses worldwide.',
                'address': 'SP Infocity, Module 1, 4th Floor, MGR Salai, Perungudi',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'zip_code': '600096',
                'phone': '+91 44 6667 8000',
                'email': 'support@freshworks.com',
                'website': 'https://freshworks.com',
                'is_verified': True,
            },

            # Category 5: Finance & Real Estate (2)
            {
                'name': 'HDFC Bank House Lower Parel',
                'category': self.categories[5],
                'owner': self.owners[10],
                'short_description': 'India’s largest private sector bank offering personal, NRI, and corporate banking.',
                'description': 'HDFC Bank House at Lower Parel provides wealth management, home loan processing desks, MSME credit facilities, and digital banking support.',
                'address': 'HDFC Bank House, Senapati Bapat Marg, Lower Parel',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'zip_code': '400013',
                'phone': '+91 22 6160 6161',
                'email': 'support@hdfcbank.com',
                'website': 'https://hdfcbank.com',
                'is_verified': True,
            },
            {
                'name': 'Prestige Estates Projects MG Road',
                'category': self.categories[5],
                'owner': self.owners[11],
                'short_description': 'Leading real estate developer of luxury residential enclaves and tech parks.',
                'description': 'Prestige Group is India’s premier property developer behind landmark tech parks, luxury apartments, and retail malls across South India.',
                'address': 'Prestige Falcon Tower, 19 Brunton Road, Off MG Road',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'zip_code': '560025',
                'phone': '+91 80 2559 1080',
                'email': 'properties@prestigeconstructions.com',
                'website': 'https://prestigeconstructions.com',
                'is_verified': True,
            },
        ]

        self.businesses = []
        for b_info in businesses_data:
            b = Business.objects.create(**b_info)
            self.businesses.append(b)

    def _create_reviews_and_evidence(self):
        self.stdout.write('  -> Creating minimum 5 evidence-backed reviews per business (60+ total reviews)...')

        review_templates = [
            # For Healthcare
            ("Painless Health Checkup & Clear Itemized Hospital Invoice", "Took my elderly parents for a full-body health checkup package. The lab staff were soft-spoken and professional. The final GST invoice clearly showed health insurance co-pay details without hidden charges.", 5, "invoice", "apollo_itemized_medical_bill.pdf", "Official GST invoice with patient ID"),
            ("Fast TPA Cashless Insurance Approval at Emergency Desk", "Visited emergency department at midnight for acute abdominal pain. The desk cleared TPA cashless insurance approval within 40 minutes. Clean ICU facilities.", 5, "document", "discharge_summary_tpa.pdf", "Discharge summary & cashless approval letter"),
            ("Professional Orthopedic Consultation & X-Ray Lab Proof", "Consulted senior orthopedic surgeon for knee joint pain. MRI and digital X-ray scans were performed promptly. Digital reports accessible on patient portal.", 4, "document", "ortho_mri_scan_report.pdf", "MRI Knee scan report & radiologist note"),
            ("Hassle-Free Pharmacy & Diagnostic Blood Test Turnaround", "Blood samples drawn at home service. Test results emailed within 6 hours. Itemized pharmacy bill provided for reimbursement.", 5, "receipt", "pharmacy_gst_receipt.jpg", "Diagnostic pharmacy purchase receipt"),
            ("Clean Infrastructure & Attentive Nursing Care", "In-patient stay for 3 days after minor surgery. Room hygiene maintained twice daily. Attaching final itemized hospital bill.", 4, "invoice", "hospital_room_bill.pdf", "Itemized hospital room stay & doctor visit invoice"),

            # For Dining
            ("Authentic Rava Idli & Filter Coffee — Stamped Receipt Attached", "Stood in the morning queue. The pure ghee Masala Dosa and hot Filter Coffee were top notch as always. Attaching our paper receipt with date timestamp.", 5, "receipt", "mtr_lalbagh_table_receipt.jpg", "Official bill receipt showing items and date"),
            ("Classic South Indian Thali Meal & Quick Table Service", "Had traditional South Indian full meal served on banana leaf. Fresh ingredients, unlimited sambar, and authentic rasam.", 5, "photo", "south_indian_thali.jpg", "Banana leaf meal presentation"),
            ("Crispy Ghee Roast Dosa & Chutney Spread", "Unmatched taste and crispy texture. Staff managed the crowd efficiently. Original printed food bill attached.", 4, "receipt", "dosa_dining_receipt.jpg", "Printed dining bill receipt"),
            ("Unforgettable Heritage Ambience & Chandrahara Dessert", "Visited with family. Tried Chandrahara dessert and Filter Coffee. Timeless heritage ambience preserved.", 5, "photo", "filter_coffee_brass.jpg", "Traditional brass cup filter coffee"),
            ("Prompt Service & Hygienic Kitchen Operations", "Clean dining tables and prompt waiter service despite heavy Sunday lunch crowd. Bill receipt verified.", 4, "receipt", "sunday_lunch_receipt.jpg", "Sunday lunch food receipt"),

            # For Electronics
            ("Smooth Laptop Purchase with GST Invoice & Brand Warranty", "Bought an Asus ROG laptop. Sales executive assisted with live benchmark testing. The tax invoice was emailed instantly for GST input claim.", 5, "invoice", "croma_tax_invoice_gst.pdf", "Croma electronic tax invoice with serial number"),
            ("Great Smart TV Demo & Next-Day Home Installation", "Purchased 55-inch OLED TV. Installation team arrived the next morning and mounted it securely. Invoice attached.", 4, "invoice", "tv_purchase_invoice.pdf", "Store tax invoice and warranty registration"),
            ("Hassle-Free Smartphone Trade-in & Instant Exchange Bonus", "Exchanged old smartphone for latest flagship model. Transparent diagnostic evaluation and instant discount applied.", 5, "receipt", "phone_exchange_receipt.jpg", "Exchange valuation receipt & invoice"),
            ("Polite Store Staff & Genuine Audio Product Demo", "Tested noise-canceling headphones in live demo booth. Transparent pricing with bank cashback discount.", 4, "photo", "unboxing_headphones.jpg", "Product box unboxing at checkout counter"),
            ("Quick Billing & Extended Warranty Protection Plan", "Purchased microwave oven. Staff explained extended warranty coverage clearly. Tax receipt attached.", 5, "invoice", "appliance_gst_invoice.pdf", "Appliance purchase invoice & warranty certificate"),

            # For Automotive
            ("Transparent Servicing & Digital Brake Inspection Report", "Gave car for 40,000 km periodic service. Service advisor sent a video inspection link showing brake pad wear before replacing them with OEM parts.", 4, "document", "maruti_service_inspection_sheet.pdf", "Digital vehicle health inspection card"),
            ("Honest Engine Oil Replacement & Automated Wheel Alignment", "Service completed on promised time. Wheel alignment report and genuine engine oil parts bill provided.", 5, "invoice", "engine_oil_parts_bill.pdf", "OEM spare parts billing receipt"),
            ("Smooth Car Delivery Experience & Complete Accessories Fitment", "Took delivery of new vehicle. Sales advisor explained all dashboard features and provided itemized accessories bill.", 5, "photo", "new_car_delivery.jpg", "New car handover ceremony photo"),
            ("Prompt Insurance Renewal & Cashless Body Repair", "Bumper scratch repair processed under cashless motor insurance. Seamless claim clearance within 2 days.", 4, "document", "insurance_claim_clearance.pdf", "Motor insurance claim approval letter"),
            ("Professional AC Servicing & Cabin Filter Replacement", "Air conditioning cooling restored. AC gas recharge and new cabin filter installed with genuine bill.", 5, "receipt", "ac_service_receipt.jpg", "AC maintenance & parts invoice"),

            # For Software
            ("Successful Enterprise Migration to Cloud CRM & Billing", "Migrated our company billing and customer workflow to cloud suite. Milestone delivery was completed cleanly within contracted timeframe.", 5, "screenshot", "cloud_crm_signoff.png", "Enterprise milestone sign-off certificate"),
            ("Outstanding Customer Support & 24/7 SLA Responsiveness", "Support team resolved our API integration query within 30 minutes. Clear documentation and responsive account manager.", 5, "document", "saas_subscription_invoice.pdf", "Enterprise annual subscription invoice"),
            ("Smooth Data Backup & Zero Downtime Cloud Deployment", "Upgraded database cluster to high-availability setup with zero downtime during peak hours.", 4, "screenshot", "system_uptime_dashboard.png", "Live system uptime report"),
            ("User-Friendly UI & Automated Financial Reporting", "Automated our monthly GST invoicing and expense tracking. Saved 15+ manual accounting hours every week.", 5, "document", "software_licensing_contract.pdf", "Software license agreement contract"),
            ("Seamless Mobile App Synchronization & Security Compliance", "Mobile app sync works smoothly offline and online. SOC2 security audit compliance verified.", 5, "screenshot", "soc2_compliance_badge.png", "Security compliance verification badge"),

            # For Finance & Real Estate
            ("Quick Home Loan Disbursement & Digital Sanction Letter", "Applied for home loan. The loan officer processed property verification documents within 5 working days. Sanction letter attached.", 5, "document", "hdfc_loan_sanction_letter.pdf", "Official home loan sanction letter"),
            ("Transparent Apartment Allotment & Flat Possession Booking", "Visited office for flat handover paperwork. Clear documentation and transparent maintenance corpus deposit breakdown provided.", 4, "document", "prestige_allotment_receipt.pdf", "Official allotment & payment receipt"),
            ("Hassle-Free Fixed Deposit Booking & High Interest Rate", "Opened digital fixed deposit through mobile app. Instant FD advice confirmation generated.", 5, "document", "fd_advice_certificate.pdf", "Fixed deposit advice certificate"),
            ("Professional Wealth Management Consultation & Portfolio Review", "Consulted dedicated financial advisor for mutual fund portfolio rebalancing. Clear fee structure.", 4, "receipt", "wealth_management_receipt.jpg", "Advisory service fee receipt"),
            ("Punctual Builder Handover & Superior Construction Quality", "Took keys to 3BHK flat. Construction quality and clubhouse amenities match promised floor plan.", 5, "photo", "flat_key_handover.jpg", "Flat key possession ceremony photo"),
        ]

        self.reviews = []

        # Ensure EVERY business gets at least 5 reviews!
        for b in self.businesses:
            # Pick relevant review templates based on business category
            cat_idx = self.categories.index(b.category)
            start_idx = (cat_idx % 6) * 5

            for r_offset in range(5):
                template_idx = start_idx + r_offset
                title, body, rating, ev_type, ev_filename, ev_caption = review_templates[template_idx % len(review_templates)]

                # Pick a distinct reviewer for each review of this business
                reviewer = self.reviewers[(b.id * 5 + r_offset) % len(self.reviewers)]

                review = Review.objects.create(
                    author=reviewer,
                    business=b,
                    title=f"{title} ({b.city})",
                    body=f"{body} Verified visit to {b.name}.",
                    visit_date=timezone.now().date() - timedelta(days=random.randint(3, 45)),
                    rating=rating,
                )

                # Attach evidence item
                Evidence.objects.create(
                    review=review,
                    original_filename=ev_filename,
                    uploaded_by=reviewer,
                    evidence_type=ev_type,
                    caption=ev_caption,
                    file_size=random.randint(220000, 2600000),
                    is_verified=True,
                )

                # Calculate Trust Score
                calculate_trust_score(review)
                self.reviews.append(review)

    def _create_community_interactions(self):
        self.stdout.write('  -> Creating community votes, comments & responses...')

        # Add Votes
        for r in self.reviews:
            for voter in self.reviewers[:4]:
                if voter != r.author:
                    Vote.objects.create(
                        user=voter,
                        review=r,
                        value=1
                    )

        # Add Official Business Responses
        for r in self.reviews[::2]: # Respond to every second review
            if r.business.owner:
                BusinessResponse.objects.create(
                    review=r,
                    responder=r.business.owner,
                    body=f'Namaste {r.author.first_name}! Thank you for choosing {r.business.name}. We appreciate your detailed proof-backed feedback.',
                    is_official=True,
                )

        # Recalculate Trust Scores after votes & responses
        for r in self.reviews:
            calculate_trust_score(r)

        # Recalculate Reviewer Reputation Scores
        for u in self.reviewers:
            if hasattr(u, 'reputation'):
                u.reputation.total_reviews = u.reviews.count()
                u.reputation.total_evidence = Evidence.objects.filter(uploaded_by=u).count()
                u.reputation.total_helpful_votes = Vote.objects.filter(review__author=u, value=1).count()
                u.reputation.recalculate()

        # Audit log entry
        AuditLog.objects.create(
            user=self.admin_user,
            action='create',
            model_name='IndianBusinessSeedMin5',
            object_id=1,
            changes={'status': 'Populated min 5 evidence reviews for every single Indian business'},
        )
