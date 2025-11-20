import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Reilly's Plumbing Portal",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .service-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .emergency-banner {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class PlumbingPortal:
    def __init__(self):
        self.services = {
            "Emergency": [
                "Burst Pipe",
                "Severe Drain Clog",
                "No Hot Water",
                "Sewage Backup",
                "Gas Line Issue"
            ],
            "Repair": [
                "Leaky Faucet",
                "Running Toilet",
                "Clogged Drain",
                "Water Heater Repair",
                "Garbage Disposal Repair"
            ],
            "Installation": [
                "Water Heater Installation",
                "Faucet Installation",
                "Toilet Installation",
                "Garbage Disposal Installation",
                "Pipe Replacement"
            ]
        }
        
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize data files if they don't exist"""
        if not os.path.exists('service_requests.json'):
            with open('service_requests.json', 'w') as f:
                json.dump([], f)
    
    def save_service_request(self, request_data):
        """Save service request to JSON file"""
        try:
            with open('service_requests.json', 'r') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
        
        request_data['timestamp'] = datetime.now().isoformat()
        request_data['request_id'] = f"REQ{datetime.now().strftime('%Y%m%d%H%M%S')}"
        existing_data.append(request_data)
        
        with open('service_requests.json', 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return request_data['request_id']
    
    def get_estimated_price_range(self, service_type, urgency):
        """Provide preliminary price estimates based on service type and urgency"""
        base_prices = {
            "Burst Pipe": {"min": 200, "max": 800},
            "Severe Drain Clog": {"min": 150, "max": 500},
            "No Hot Water": {"min": 100, "max": 600},
            "Leaky Faucet": {"min": 75, "max": 250},
            "Running Toilet": {"min": 50, "max": 200},
            "Water Heater Installation": {"min": 800, "max": 2500}
        }
        
        # Adjust for emergency service
        emergency_multiplier = 1.5 if urgency == "Emergency - Water Everywhere!" else 1.0
        
        if service_type in base_prices:
            min_price = base_prices[service_type]["min"] * emergency_multiplier
            max_price = base_prices[service_type]["max"] * emergency_multiplier
            return f"${int(min_price)} - ${int(max_price)}"
        
        return "$150 - $500"  # Default range

def main():
    portal = PlumbingPortal()
    
    # Header
    st.markdown('<div class="main-header">🔧 Reilly\'s Plumbing Service Portal</div>', unsafe_allow_html=True)
    
    # Emergency banner
    st.markdown("""
    <div class="emergency-banner">
    🚨 24/7 EMERGENCY SERVICE AVAILABLE 🚨<br>
    Call Now: <strong>(510) 690-5197</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["📋 Request Service", "ℹ️ Service Info", "📞 Contact Us"])
    
    with tab1:
        st.subheader("Schedule Your Service Request")
        
        with st.form("service_request_form"):
            # Customer Information
            st.write("### Your Information")
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name *", placeholder="John Smith")
                email = st.text_input("Email Address *", placeholder="john@example.com")
                
            with col2:
                phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
                address = st.text_input("Service Address *", placeholder="123 Main St, San Jose, CA")
            
            # Service Details
            st.write("### Service Details")
            
            # Service category and type
            service_category = st.selectbox(
                "Service Category *",
                ["Emergency", "Repair", "Installation"]
            )
            
            service_type = st.selectbox(
                "Specific Service Needed *",
                portal.services[service_category]
            )
            
            # Urgency level
            urgency = st.select_slider(
                "How urgent is this? *",
                options=[
                    "Scheduled Check-up",
                    "Minor Issue - Can Wait", 
                    "Need Soon",
                    "Urgent - Within 24 Hours",
                    "Emergency - Water Everywhere!"
                ],
                value="Need Soon"
            )
            
            # Description and photo upload
            description = st.text_area(
                "Please describe the problem in detail *",
                placeholder="Example: Kitchen sink has been draining slowly for 2 days, now completely clogged. Water backs up when running disposal.",
                height=100
            )
            
            # Photo upload
            uploaded_file = st.file_uploader(
                "Upload a photo of the problem (optional, but very helpful)",
                type=['png', 'jpg', 'jpeg'],
                help="Photos help us diagnose the issue faster and bring the right tools."
            )
            
            # Preferred contact time
            contact_time = st.selectbox(
                "Best time to contact you",
                ["Anytime", "Morning (8AM-12PM)", "Afternoon (12PM-5PM)", "Evening (5PM-8PM)"]
            )
            
            # Terms and submission
            agree_terms = st.checkbox(
                "I agree to be contacted by Reilly's Plumbing regarding this service request *"
            )
            
            submitted = st.form_submit_button("Submit Service Request", type="primary")
            
            if submitted:
                # Basic validation
                if not all([full_name, email, phone, address, description, agree_terms]):
                    st.error("Please fill in all required fields (*) and agree to the terms.")
                else:
                    # Prepare request data
                    request_data = {
                        "customer_info": {
                            "full_name": full_name,
                            "email": email,
                            "phone": phone,
                            "address": address
                        },
                        "service_details": {
                            "category": service_category,
                            "type": service_type,
                            "urgency": urgency,
                            "description": description,
                            "contact_preference": contact_time
                        },
                        "photo_uploaded": uploaded_file is not None,
                        "preliminary_price_range": portal.get_estimated_price_range(service_type, urgency)
                    }
                    
                    # Save the request
                    request_id = portal.save_service_request(request_data)
                    
                    # Show success message
                    st.markdown(f"""
                    <div class="success-message">
                    <h3>✅ Service Request Submitted Successfully!</h3>
                    <p><strong>Request ID:</strong> {request_id}</p>
                    <p>We've received your request and will contact you within the next hour to confirm details and schedule your service.</p>
                    <p><strong>Preliminary Price Range:</strong> {request_data['preliminary_price_range']}</p>
                    <p><em>Note: Final pricing may vary after on-site assessment.</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show next steps
                    with st.expander("What happens next?"):
                        st.write("""
                        1. **Immediate Confirmation**: You'll receive a text/email confirmation within minutes
                        2. **Quick Phone Call**: Our dispatcher will call to confirm details and schedule
                        3. **Service Dispatch**: We'll send a licensed plumber with the right tools and parts
                        4. **Transparent Pricing**: You'll receive the final quote before any work begins
                        """)
    
    with tab2:
        st.subheader("Our Services & Pricing")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🚨 Emergency Services")
            for service in portal.services["Emergency"]:
                with st.container():
                    st.markdown(f"**{service}**")
                    st.caption("Available 24/7 - Immediate Response")
                    st.write("---")
        
        with col2:
            st.markdown("### 🔧 Repair Services")
            for service in portal.services["Repair"]:
                with st.container():
                    st.markdown(f"**{service}**")
                    st.caption("Same-day service available")
                    st.write("---")
        
        with col3:
            st.markdown("### 🏠 Installation Services")
            for service in portal.services["Installation"]:
                with st.container():
                    st.markdown(f"**{service}**")
                    st.caption("Professional installation & warranty")
                    st.write("---")
        
        st.info("💡 **All services include free, no-obligation estimates. Final pricing provided before work begins.**")
    
    with tab3:
        st.subheader("Contact Reilly's Plumbing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📞 Immediate Help")
            st.write("""
            **24/7 Emergency Line**  
            **(510) 690-5197**
            
            **Office Hours**  
            Monday - Friday: 7:00 AM - 7:00 PM  
            Saturday: 8:00 AM - 5:00 PM  
            Sunday: Emergency Service Only
            """)
            
            st.markdown("### 📍 Service Area")
            st.write("""
            Serving the entire South Bay Area:
            - San Jose
            - Santa Clara
            - Campbell
            - Los Gatos
            - Saratoga
            - And surrounding communities
            """)
        
        with col2:
            st.markdown("### ✉️ Send Us a Message")
            
            with st.form("contact_form"):
                contact_name = st.text_input("Your Name")
                contact_phone = st.text_input("Phone Number")
                contact_message = st.text_area("Message", height=120)
                
                if st.form_submit_button("Send Message"):
                    st.success("Message sent! We'll respond within 2 hours during business hours.")

if __name__ == "__main__":
    main()
