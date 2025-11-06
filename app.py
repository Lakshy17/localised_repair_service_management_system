import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Repair Service Management System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    h2 {
        color: #2c3e50;
        padding-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Database connection function
def get_database_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Change this to your MySQL username
            password="Mysql@2025",  # Change this to your MySQL password
            database="repair_service_db",
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

def execute_query(query, params=None, fetch=True):
    """Execute a query and return results"""
    conn = get_database_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = True
        
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        st.error(f"Query execution error: {err}")
        if conn and conn.is_connected():
            conn.close()
        return None

# ==================== DASHBOARD PAGE ====================
def dashboard_page():
    st.title("Dashboard")
    st.markdown("### System Overview")
    
    # Fetch summary statistics
    total_users = execute_query("SELECT COUNT(*) as count FROM User")[0]['count']
    total_technicians = execute_query("SELECT COUNT(*) as count FROM Technician")[0]['count']
    total_requests = execute_query("SELECT COUNT(*) as count FROM Repair_Request")[0]['count']
    pending_requests = execute_query("SELECT COUNT(*) as count FROM Repair_Request WHERE status = 'pending'")[0]['count']
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", total_users, delta=None)
    with col2:
        st.metric("Total Technicians", total_technicians, delta=None)
    with col3:
        st.metric("Total Requests", total_requests, delta=None)
    with col4:
        st.metric("Pending Requests", pending_requests, delta=None)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests by Status")
        status_data = execute_query("""
            SELECT status, COUNT(*) as count 
            FROM Repair_Request 
            GROUP BY status
        """)
        if status_data:
            df_status = pd.DataFrame(status_data)
            fig = px.pie(df_status, values='count', names='status', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Service Category")
        revenue_data = execute_query("""
            SELECT sc.category_name, SUM(p.payment_amount) as total_revenue
            FROM Payment p
            JOIN Service_Assignment sa ON p.assignment_id = sa.assignment_id
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
            WHERE p.payment_status = 'completed'
            GROUP BY sc.category_name
        """)
        if revenue_data:
            df_revenue = pd.DataFrame(revenue_data)
            fig = px.bar(df_revenue, x='category_name', y='total_revenue',
                        color='total_revenue', color_continuous_scale='Blues')
            fig.update_layout(xaxis_title="Service Category", yaxis_title="Revenue (₹)")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Repair Requests")
    recent_requests = execute_query("""
        SELECT rr.request_id, u.first_name, u.last_name, sc.category_name,
               rr.status, rr.request_date
        FROM Repair_Request rr
        JOIN User u ON rr.customer_id = u.user_id
        JOIN Service_Category sc ON rr.category_id = sc.category_id
        ORDER BY rr.request_date DESC
        LIMIT 10
    """)
    if recent_requests:
        df_recent = pd.DataFrame(recent_requests)
        st.dataframe(df_recent, use_container_width=True)

# ==================== LOCATION MANAGEMENT ====================
def location_management():
    st.title("Location Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update", "Delete"])
    
    with tab1:
        st.subheader("All Locations")
        locations = execute_query("SELECT * FROM Location ORDER BY location_id")
        if locations:
            df = pd.DataFrame(locations)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Location")
        with st.form("add_location_form"):
            area_name = st.text_input("Area Name *")
            city = st.text_input("City *")
            state = st.text_input("State *")
            pincode = st.text_input("Pincode *")
            delivery_charge = st.number_input("Delivery Charge (₹)", min_value=0.0, value=50.0, step=10.0)
            
            submitted = st.form_submit_button("Add Location")
            if submitted:
                if area_name and city and state and pincode:
                    query = "INSERT INTO Location (area_name, city, state, pincode, delivery_charge) VALUES (%s, %s, %s, %s, %s)"
                    if execute_query(query, (area_name, city, state, pincode, delivery_charge), fetch=False):
                        st.success("Location added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill all required fields")
    
    with tab3:
        st.subheader("Update Location")
        locations = execute_query("SELECT * FROM Location")
        if locations:
            location_ids = [loc['location_id'] for loc in locations]
            selected_id = st.selectbox("Select Location ID", location_ids)
            
            selected_loc = next((loc for loc in locations if loc['location_id'] == selected_id), None)
            
            if selected_loc:
                with st.form("update_location_form"):
                    area_name = st.text_input("Area Name", value=selected_loc['area_name'])
                    city = st.text_input("City", value=selected_loc['city'])
                    state = st.text_input("State", value=selected_loc['state'])
                    pincode = st.text_input("Pincode", value=selected_loc['pincode'])
                    delivery_charge = st.number_input("Delivery Charge (₹)", value=float(selected_loc['delivery_charge']))
                    
                    submitted = st.form_submit_button("Update Location")
                    if submitted:
                        query = "UPDATE Location SET area_name=%s, city=%s, state=%s, pincode=%s, delivery_charge=%s WHERE location_id=%s"
                        if execute_query(query, (area_name, city, state, pincode, delivery_charge, selected_id), fetch=False):
                            st.success("Location updated successfully!")
                            st.rerun()
    
    with tab4:
        st.subheader("Delete Location")
        locations = execute_query("SELECT * FROM Location")
        if locations:
            location_ids = [loc['location_id'] for loc in locations]
            selected_id = st.selectbox("Select Location ID to Delete", location_ids)
            
            if st.button("🗑️ Delete Location", type="primary"):
                query = "DELETE FROM Location WHERE location_id = %s"
                if execute_query(query, (selected_id,), fetch=False):
                    st.success("Location deleted successfully!")
                    st.rerun()

# ==================== USER MANAGEMENT ====================
def user_management():
    st.title("User Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update", "Delete"])
    
    with tab1:
        st.subheader("All Users")
        users = execute_query("""
            SELECT u.*, l.city, l.state 
            FROM User u 
            LEFT JOIN Location l ON u.location_id = l.location_id
            ORDER BY u.user_id
        """)
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New User")
        locations = execute_query("SELECT location_id, area_name, city, state FROM Location")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *")
                last_name = st.text_input("Last Name *")
                email = st.text_input("Email *")
                phone = st.text_input("Phone Number *")
            with col2:
                street = st.text_input("Street")
                user_type = st.selectbox("User Type *", ["customer", "technician"])
                if locations:
                    location_options = {f"{loc['area_name']}, {loc['city']}, {loc['state']}": loc['location_id'] for loc in locations}
                    selected_location = st.selectbox("Location *", options=list(location_options.keys()))
                    location_id = location_options[selected_location]
            
            submitted = st.form_submit_button("Add User")
            if submitted:
                if all([first_name, last_name, email, phone]):
                    # Get city, state, pincode from selected location
                    loc_data = next(loc for loc in locations if loc['location_id'] == location_id)
                    query = """INSERT INTO User (first_name, last_name, email, phone_number, street, city, state, pincode, registration_date, user_type, location_id) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    if execute_query(query, (first_name, last_name, email, phone, street, loc_data['city'], 
                                           loc_data['state'], '560001', date.today(), user_type, location_id), fetch=False):
                        st.success("User added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill all required fields")
    
    with tab3:
        st.subheader("Update User")
        users = execute_query("SELECT * FROM User")
        locations = execute_query("SELECT location_id, area_name, city, state FROM Location")
        
        if users:
            user_ids = [user['user_id'] for user in users]
            selected_id = st.selectbox("Select User ID", user_ids)
            
            selected_user = next((user for user in users if user['user_id'] == selected_id), None)
            
            if selected_user:
                with st.form("update_user_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", value=selected_user['first_name'])
                        last_name = st.text_input("Last Name", value=selected_user['last_name'])
                        email = st.text_input("Email", value=selected_user['email'])
                    with col2:
                        phone = st.text_input("Phone Number", value=selected_user['phone_number'])
                        street = st.text_input("Street", value=selected_user['street'] or "")
                        if locations:
                            location_options = {f"{loc['area_name']}, {loc['city']}, {loc['state']}": loc['location_id'] for loc in locations}
                            current_loc_idx = list(location_options.values()).index(selected_user['location_id'])
                            selected_location = st.selectbox("Location", 
                                                            options=list(location_options.keys()),
                                                            index=current_loc_idx)
                            location_id = location_options[selected_location]
                    
                    submitted = st.form_submit_button("Update User")
                    if submitted:
                        query = """UPDATE User SET first_name=%s, last_name=%s, email=%s, 
                                   phone_number=%s, street=%s, location_id=%s WHERE user_id=%s"""
                        if execute_query(query, (first_name, last_name, email, phone, street, location_id, selected_id), fetch=False):
                            st.success("User updated successfully!")
                            st.rerun()
    
    with tab4:
        st.subheader("Delete User")
        users = execute_query("SELECT user_id, first_name, last_name, email FROM User")
        if users:
            user_options = {f"{user['user_id']} - {user['first_name']} {user['last_name']} ({user['email']})": 
                          user['user_id'] for user in users}
            selected_user = st.selectbox("Select User to Delete", options=list(user_options.keys()))
            user_id = user_options[selected_user]
            
            if st.button("🗑️ Delete User", type="primary"):
                query = "DELETE FROM User WHERE user_id = %s"
                if execute_query(query, (user_id,), fetch=False):
                    st.success("User deleted successfully!")
                    st.rerun()

# ==================== TECHNICIAN MANAGEMENT ====================
def technician_management():
    st.title("Technician Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update", "Delete"])
    
    with tab1:
        st.subheader("All Technicians")
        technicians = execute_query("""
            SELECT t.technician_id, t.user_id, u.first_name, u.last_name, u.email, u.phone_number,
                   t.experience_years, t.availability_status, t.certification_details,
                   GROUP_CONCAT(ts.specialization SEPARATOR ', ') as specializations
            FROM Technician t
            JOIN User u ON t.user_id = u.user_id
            LEFT JOIN Technician_Specialization ts ON t.technician_id = ts.technician_id
            GROUP BY t.technician_id
            ORDER BY t.technician_id
        """)
        if technicians:
            df = pd.DataFrame(technicians)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Technician")
        # Get users who are technicians but not yet in Technician table
        available_users = execute_query("""
            SELECT u.user_id, u.first_name, u.last_name, u.email 
            FROM User u 
            WHERE u.user_type = 'technician' 
            AND u.user_id NOT IN (SELECT user_id FROM Technician)
        """)
        
        if available_users:
            with st.form("add_technician_form"):
                user_options = {f"{u['first_name']} {u['last_name']} ({u['email']})": u['user_id'] for u in available_users}
                selected_user = st.selectbox("Select User *", options=list(user_options.keys()))
                user_id = user_options[selected_user]
                
                col1, col2 = st.columns(2)
                with col1:
                    experience = st.number_input("Experience (years) *", min_value=0, max_value=50)
                    certification = st.text_area("Certification Details")
                with col2:
                    availability = st.selectbox("Availability *", ["available", "busy", "offline"])
                    specializations = st.text_input("Specializations (comma-separated) *", 
                                                   placeholder="e.g., Smartphone Repair, Laptop Repair")
                
                submitted = st.form_submit_button("Add Technician")
                if submitted:
                    if experience is not None and specializations:
                        # Insert technician
                        query = """INSERT INTO Technician (user_id, experience_years, certification_details, 
                                   availability_status, created_date) 
                                   VALUES (%s, %s, %s, %s, %s)"""
                        if execute_query(query, (user_id, experience, certification, availability, date.today()), fetch=False):
                            # Get the last inserted technician_id
                            tech_id = execute_query("SELECT LAST_INSERT_ID() as id")[0]['id']
                            
                            # Insert specializations
                            spec_list = [s.strip() for s in specializations.split(',')]
                            for spec in spec_list:
                                spec_query = "INSERT INTO Technician_Specialization (technician_id, specialization) VALUES (%s, %s)"
                                execute_query(spec_query, (tech_id, spec), fetch=False)
                            
                            st.success("Technician added successfully!")
                            st.rerun()
                    else:
                        st.error("Please fill all required fields")
        else:
            st.info("No available users with type 'technician'. Please add a user first with user_type='technician'.")
    
    with tab3:
        st.subheader("Update Technician")
        technicians = execute_query("""
            SELECT t.*, u.first_name, u.last_name 
            FROM Technician t 
            JOIN User u ON t.user_id = u.user_id
        """)
        
        if technicians:
            tech_options = {f"{t['technician_id']} - {t['first_name']} {t['last_name']}": t['technician_id'] for t in technicians}
            selected_id = st.selectbox("Select Technician", list(tech_options.keys()))
            tech_id = tech_options[selected_id]
            
            selected_tech = next((tech for tech in technicians if tech['technician_id'] == tech_id), None)
            
            if selected_tech:
                with st.form("update_technician_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        experience = st.number_input("Experience (years)", value=selected_tech['experience_years'])
                        certification = st.text_area("Certification Details", value=selected_tech['certification_details'] or "")
                    with col2:
                        current_avail_idx = ["available", "busy", "offline"].index(selected_tech['availability_status'])
                        availability = st.selectbox("Availability", ["available", "busy", "offline"], 
                                                   index=current_avail_idx)
                    
                    submitted = st.form_submit_button("Update Technician")
                    if submitted:
                        query = """UPDATE Technician SET experience_years=%s, certification_details=%s, 
                                   availability_status=%s WHERE technician_id=%s"""
                        if execute_query(query, (experience, certification, availability, tech_id), fetch=False):
                            st.success("Technician updated successfully!")
                            st.rerun()
    
    with tab4:
        st.subheader("Delete Technician")
        technicians = execute_query("""
            SELECT t.technician_id, u.first_name, u.last_name, u.email 
            FROM Technician t 
            JOIN User u ON t.user_id = u.user_id
        """)
        if technicians:
            tech_options = {f"{tech['technician_id']} - {tech['first_name']} {tech['last_name']} ({tech['email']})": 
                          tech['technician_id'] for tech in technicians}
            selected_tech = st.selectbox("Select Technician to Delete", options=list(tech_options.keys()))
            tech_id = tech_options[selected_tech]
            
            if st.button("Delete Technician", type="primary"):
                query = "DELETE FROM Technician WHERE technician_id = %s"
                if execute_query(query, (tech_id,), fetch=False):
                    st.success("Technician deleted successfully!")
                    st.rerun()

# ==================== SERVICE CATEGORY MANAGEMENT ====================
def service_category_management():
    st.title("Service Category Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update", "Delete"])
    
    with tab1:
        st.subheader("All Service Categories")
        categories = execute_query("""
            SELECT sc.*, COUNT(DISTINCT rr.request_id) as request_count
            FROM Service_Category sc
            LEFT JOIN Repair_Request rr ON sc.category_id = rr.category_id
            GROUP BY sc.category_id
            ORDER BY sc.category_id
        """)
        if categories:
            df = pd.DataFrame(categories)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Service Category")
        with st.form("add_category_form"):
            category_name = st.text_input("Category Name *")
            description = st.text_area("Description")
            base_charge = st.number_input("Base Service Charge (₹) *", min_value=0.0, step=100.0)
            estimated_hours = st.number_input("Estimated Time (hours) *", min_value=1, value=2)
            
            submitted = st.form_submit_button("Add Category")
            if submitted:
                if category_name and base_charge:
                    query = """INSERT INTO Service_Category (category_name, category_description, 
                               base_service_charge, estimated_time_hours) VALUES (%s, %s, %s, %s)"""
                    if execute_query(query, (category_name, description, base_charge, estimated_hours), fetch=False):
                        st.success("Service category added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill all required fields")
    
    with tab3:
        st.subheader("Update Service Category")
        categories = execute_query("SELECT * FROM Service_Category")
        if categories:
            category_ids = [cat['category_id'] for cat in categories]
            selected_id = st.selectbox("Select Category ID", category_ids)
            
            selected_cat = next((cat for cat in categories if cat['category_id'] == selected_id), None)
            
            if selected_cat:
                with st.form("update_category_form"):
                    category_name = st.text_input("Category Name", value=selected_cat['category_name'])
                    description = st.text_area("Description", value=selected_cat['category_description'] or "")
                    base_charge = st.number_input("Base Service Charge (₹)", value=float(selected_cat['base_service_charge']))
                    estimated_hours = st.number_input("Estimated Time (hours)", value=selected_cat['estimated_time_hours'])
                    
                    submitted = st.form_submit_button("Update Category")
                    if submitted:
                        query = """UPDATE Service_Category SET category_name=%s, category_description=%s, 
                                   base_service_charge=%s, estimated_time_hours=%s WHERE category_id=%s"""
                        if execute_query(query, (category_name, description, base_charge, estimated_hours, selected_id), fetch=False):
                            st.success("Service category updated successfully!")
                            st.rerun()
    
    with tab4:
        st.subheader("Delete Service Category")
        categories = execute_query("SELECT category_id, category_name, base_service_charge FROM Service_Category")
        if categories:
            cat_options = {f"{cat['category_id']} - {cat['category_name']} (₹{cat['base_service_charge']})": 
                         cat['category_id'] for cat in categories}
            selected_cat = st.selectbox("Select Category to Delete", options=list(cat_options.keys()))
            cat_id = cat_options[selected_cat]
            
            if st.button("Delete Category", type="primary"):
                query = "DELETE FROM Service_Category WHERE category_id = %s"
                if execute_query(query, (cat_id,), fetch=False):
                    st.success("Service category deleted successfully!")
                    st.rerun()

# ==================== REPAIR REQUEST MANAGEMENT ====================
def repair_request_management():
    st.title("Repair Request Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update Status", "Delete"])
    
    with tab1:
        st.subheader("All Repair Requests")
        requests = execute_query("""
            SELECT rr.*, u.first_name, u.last_name, u.email, 
                   sc.category_name, l.city, l.state
            FROM Repair_Request rr
            JOIN User u ON rr.customer_id = u.user_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
            JOIN Location l ON u.location_id = l.location_id
            ORDER BY rr.request_date DESC
        """)
        if requests:
            df = pd.DataFrame(requests)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Repair Request")
        users = execute_query("SELECT user_id, first_name, last_name, email FROM User WHERE user_type = 'customer'")
        categories = execute_query("SELECT category_id, category_name FROM Service_Category")
        
        with st.form("add_request_form"):
            col1, col2 = st.columns(2)
            with col1:
                if users:
                    user_options = {f"{user['first_name']} {user['last_name']} ({user['email']})": 
                                  user['user_id'] for user in users}
                    selected_user = st.selectbox("Customer *", options=list(user_options.keys()))
                    customer_id = user_options[selected_user]
                
                if categories:
                    category_options = {cat['category_name']: cat['category_id'] for cat in categories}
                    selected_category = st.selectbox("Service Category *", options=list(category_options.keys()))
                    category_id = category_options[selected_category]
                
                item_description = st.text_area("Item Description *")
                issue_description = st.text_area("Issue Description *")
            
            with col2:
                priority = st.selectbox("Priority *", ["low", "medium", "high", "urgent"])
                preferred_date = st.date_input("Preferred Date", value=date.today())
                status = st.selectbox("Status *", ["pending", "assigned", "in_progress", "completed", "cancelled"])
            
            submitted = st.form_submit_button("Add Request")
            if submitted:
                if all([customer_id, category_id, item_description, issue_description]):
                    query = """INSERT INTO Repair_Request (customer_id, category_id, item_description, 
                               issue_description, priority_level, request_date, preferred_date, status) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    if execute_query(query, (customer_id, category_id, item_description, issue_description,
                                           priority, datetime.now(), preferred_date, status), fetch=False):
                        st.success("Repair request added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill all required fields")
    
    with tab3:
        st.subheader("Update Request Status")
        requests = execute_query("""
            SELECT rr.request_id, rr.item_description, rr.status,
                   u.first_name, u.last_name, sc.category_name
            FROM Repair_Request rr
            JOIN User u ON rr.customer_id = u.user_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
            ORDER BY rr.request_date DESC
        """)
        
        if requests:
            request_options = {
                f"Request #{req['request_id']} - {req['first_name']} {req['last_name']} - {req['category_name']} ({req['status']})": 
                req['request_id'] for req in requests
            }
            selected_request = st.selectbox("Select Request", options=list(request_options.keys()))
            request_id = request_options[selected_request]
            
            selected_req = next((req for req in requests if req['request_id'] == request_id), None)
            
            if selected_req:
                with st.form("update_status_form"):
                    current_status_idx = ["pending", "assigned", "in_progress", "completed", "cancelled"].index(selected_req['status'])
                    new_status = st.selectbox("New Status", ["pending", "assigned", "in_progress", "completed", "cancelled"],
                                            index=current_status_idx)
                    
                    submitted = st.form_submit_button("Update Status")
                    if submitted:
                        query = "UPDATE Repair_Request SET status = %s WHERE request_id = %s"
                        if execute_query(query, (new_status, request_id), fetch=False):
                            st.success("Request status updated successfully!")
                            st.rerun()
    
    with tab4:
        st.subheader("Delete Repair Request")
        requests = execute_query("""
            SELECT rr.request_id, rr.item_description, u.first_name, u.last_name, sc.category_name
            FROM Repair_Request rr
            JOIN User u ON rr.customer_id = u.user_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
        """)
        
        if requests:
            request_options = {
                f"Request #{req['request_id']} - {req['first_name']} {req['last_name']} - {req['category_name']}": 
                req['request_id'] for req in requests
            }
            selected_request = st.selectbox("Select Request to Delete", options=list(request_options.keys()))
            request_id = request_options[selected_request]
            
            if st.button("Delete Request", type="primary"):
                query = "DELETE FROM Repair_Request WHERE request_id = %s"
                if execute_query(query, (request_id,), fetch=False):
                    st.success("Repair request deleted successfully!")
                    st.rerun()

# ==================== SERVICE ASSIGNMENT ====================
def service_assignment():
    st.title("Service Assignment")
    
    tab1, tab2 = st.tabs(["View Assignments", "Create Assignment"])
    
    with tab1:
        st.subheader("All Service Assignments")
        assignments = execute_query("""
            SELECT sa.*, rr.item_description, rr.status as request_status,
                   t.technician_id, u1.first_name as tech_first_name, u1.last_name as tech_last_name,
                   u2.first_name as customer_first_name, u2.last_name as customer_last_name,
                   sc.category_name
            FROM Service_Assignment sa
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN Technician t ON sa.technician_id = t.technician_id
            JOIN User u1 ON t.user_id = u1.user_id
            JOIN User u2 ON rr.customer_id = u2.user_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
            ORDER BY sa.assignment_date DESC
        """)
        if assignments:
            df = pd.DataFrame(assignments)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Create New Assignment")
        
        # Get pending requests
        pending_requests = execute_query("""
            SELECT rr.request_id, rr.item_description, u.first_name, u.last_name, 
                   sc.category_name, rr.status
            FROM Repair_Request rr
            JOIN User u ON rr.customer_id = u.user_id
            JOIN Service_Category sc ON rr.category_id = sc.category_id
            WHERE rr.status = 'pending'
            AND rr.request_id NOT IN (SELECT request_id FROM Service_Assignment)
            ORDER BY rr.request_date DESC
        """)
        
        # Get available technicians
        available_techs = execute_query("""
            SELECT t.technician_id, u.first_name, u.last_name, t.experience_years,
                   GROUP_CONCAT(ts.specialization SEPARATOR ', ') as specializations
            FROM Technician t
            JOIN User u ON t.user_id = u.user_id
            LEFT JOIN Technician_Specialization ts ON t.technician_id = ts.technician_id
            WHERE t.availability_status = 'available'
            GROUP BY t.technician_id
        """)
        
        if pending_requests and available_techs:
            with st.form("create_assignment_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    request_options = {
                        f"Request #{req['request_id']} - {req['first_name']} {req['last_name']} - {req['category_name']}": 
                        req['request_id'] for req in pending_requests
                    }
                    selected_request = st.selectbox("Select Request *", options=list(request_options.keys()))
                    request_id = request_options[selected_request]
                
                with col2:
                    tech_options = {
                        f"Tech #{tech['technician_id']} - {tech['first_name']} {tech['last_name']} ({tech['experience_years']} yrs)": 
                        tech['technician_id'] for tech in available_techs
                    }
                    selected_tech = st.selectbox("Select Technician *", options=list(tech_options.keys()))
                    technician_id = tech_options[selected_tech]
                
                service_cost = st.number_input("Service Cost (₹) *", min_value=0.0, step=100.0)
                estimated_completion = st.date_input("Estimated Completion Date *", value=date.today())
                
                submitted = st.form_submit_button("Create Assignment")
                if submitted:
                    if request_id and technician_id and service_cost > 0:
                        query = """INSERT INTO Service_Assignment (request_id, technician_id, assignment_date, 
                                   estimated_completion_date, assignment_status, service_cost) 
                                   VALUES (%s, %s, %s, %s, %s, %s)"""
                        if execute_query(query, (request_id, technician_id, datetime.now(), 
                                              estimated_completion, 'assigned', service_cost), fetch=False):
                            # Update request status
                            execute_query("UPDATE Repair_Request SET status = 'assigned' WHERE request_id = %s", 
                                        (request_id,), fetch=False)
                            # Update technician availability
                            execute_query("UPDATE Technician SET availability_status = 'busy' WHERE technician_id = %s", 
                                        (technician_id,), fetch=False)
                            
                            st.success("Assignment created successfully!")
                            st.rerun()
                    else:
                        st.error("Please fill all required fields")
        else:
            if not pending_requests:
                st.info("No pending requests available for assignment")
            if not available_techs:
                st.warning("No available technicians")

# ==================== PAYMENT MANAGEMENT ====================
def payment_management():
    st.title("Payment Management")
    
    tab1, tab2, tab3 = st.tabs(["View Payments", "Add Payment", "Payment Analytics"])
    
    with tab1:
        st.subheader("All Payments")
        payments = execute_query("""
            SELECT p.*, sa.assignment_id, rr.item_description,
                   u1.first_name as customer_first_name, u1.last_name as customer_last_name,
                   u2.first_name as tech_first_name, u2.last_name as tech_last_name
            FROM Payment p
            JOIN Service_Assignment sa ON p.assignment_id = sa.assignment_id
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN User u1 ON rr.customer_id = u1.user_id
            JOIN Technician t ON sa.technician_id = t.technician_id
            JOIN User u2 ON t.user_id = u2.user_id
            ORDER BY p.payment_date DESC
        """)
        if payments:
            df = pd.DataFrame(payments)
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            total_payments = sum(p['payment_amount'] for p in payments)
            completed_payments = sum(p['payment_amount'] for p in payments if p['payment_status'] == 'completed')
            pending_payments = sum(p['payment_amount'] for p in payments if p['payment_status'] == 'pending')
            
            with col1:
                st.metric("Total Payments", f"₹{total_payments:,.2f}")
            with col2:
                st.metric("Completed", f"₹{completed_payments:,.2f}")
            with col3:
                st.metric("Pending", f"₹{pending_payments:,.2f}")
    
    with tab2:
        st.subheader("Add New Payment")
        
        # Get assignments without payments
        assignments = execute_query("""
            SELECT sa.assignment_id, rr.item_description, 
                   u1.first_name as customer_first_name, u1.last_name as customer_last_name,
                   u2.first_name as tech_first_name, u2.last_name as tech_last_name,
                   sa.service_cost
            FROM Service_Assignment sa
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN User u1 ON rr.customer_id = u1.user_id
            JOIN Technician t ON sa.technician_id = t.technician_id
            JOIN User u2 ON t.user_id = u2.user_id
            WHERE sa.assignment_id NOT IN (SELECT assignment_id FROM Payment)
            ORDER BY sa.assignment_date DESC
        """)
        
        if assignments:
            with st.form("add_payment_form"):
                assignment_options = {
                    f"Assignment #{asg['assignment_id']} - {asg['customer_first_name']} {asg['customer_last_name']} (Tech: {asg['tech_first_name']} {asg['tech_last_name']}) - Cost: ₹{asg['service_cost']}": 
                    asg for asg in assignments
                }
                selected_assignment = st.selectbox("Select Assignment *", options=list(assignment_options.keys()))
                assignment_data = assignment_options[selected_assignment]
                
                col1, col2 = st.columns(2)
                with col1:
                    payment_amount = st.number_input("Payment Amount (₹) *", value=float(assignment_data['service_cost']), min_value=0.0, step=100.0)
                    payment_method = st.selectbox("Payment Method *", ["cash", "card", "upi", "wallet"])
                with col2:
                    payment_status = st.selectbox("Payment Status *", ["pending", "completed", "failed", "refunded"])
                    transaction_ref = st.text_input("Transaction Reference")
                
                submitted = st.form_submit_button("Add Payment")
                if submitted:
                    query = """INSERT INTO Payment (assignment_id, payment_amount, payment_method, 
                               payment_date, payment_status, transaction_reference) 
                               VALUES (%s, %s, %s, %s, %s, %s)"""
                    if execute_query(query, (assignment_data['assignment_id'], payment_amount, payment_method, 
                                           datetime.now(), payment_status, transaction_ref), fetch=False):
                        st.success("Payment added successfully!")
                        st.rerun()
        else:
            st.info("No assignments available for payment")
    
    with tab3:
        st.subheader("Payment Analytics")
        
        # Payment method distribution
        method_data = execute_query("""
            SELECT payment_method, COUNT(*) as count, SUM(payment_amount) as total
            FROM Payment
            WHERE payment_status = 'completed'
            GROUP BY payment_method
        """)
        
        if method_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Payment Methods Distribution**")
                df_method = pd.DataFrame(method_data)
                fig = px.pie(df_method, values='count', names='payment_method',
                           title="Payments by Method")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Revenue by Payment Method**")
                fig = px.bar(df_method, x='payment_method', y='total',
                           title="Revenue by Payment Method")
                fig.update_layout(xaxis_title="Payment Method", yaxis_title="Revenue (₹)")
                st.plotly_chart(fig, use_container_width=True)
        
        # Monthly revenue trend
        monthly_data = execute_query("""
            SELECT DATE_FORMAT(payment_date, '%%Y-%%m') as month, 
                   SUM(payment_amount) as revenue, COUNT(*) as transaction_count
            FROM Payment
            WHERE payment_status = 'completed'
            GROUP BY month
            ORDER BY month
        """)
        
        if monthly_data:
            st.markdown("**Monthly Revenue Trend**")
            df_monthly = pd.DataFrame(monthly_data)
            fig = px.line(df_monthly, x='month', y='revenue', markers=True,
                         title="Monthly Revenue Trend")
            fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)")
            st.plotly_chart(fig, use_container_width=True)

# ==================== REVIEW MANAGEMENT ====================
def review_management():
    st.title("Review Management")
    
    tab1, tab2, tab3 = st.tabs(["View Reviews", "Add Review", "Analytics"])
    
    with tab1:
        st.subheader("All Reviews")
        reviews = execute_query("""
            SELECT r.*, sa.assignment_id, rr.item_description,
                   u1.first_name as customer_first_name, u1.last_name as customer_last_name,
                   u2.first_name as tech_first_name, u2.last_name as tech_last_name
            FROM Review r
            JOIN Service_Assignment sa ON r.assignment_id = sa.assignment_id
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN User u1 ON rr.customer_id = u1.user_id
            JOIN Technician t ON sa.technician_id = t.technician_id
            JOIN User u2 ON t.user_id = u2.user_id
            ORDER BY r.review_date DESC
        """)
        if reviews:
            df = pd.DataFrame(reviews)
            st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Review")
        
        # Get completed assignments without reviews
        assignments = execute_query("""
            SELECT sa.assignment_id, rr.item_description, 
                   u1.first_name as customer_first_name, u1.last_name as customer_last_name,
                   u2.first_name as tech_first_name, u2.last_name as tech_last_name
            FROM Service_Assignment sa
            JOIN Repair_Request rr ON sa.request_id = rr.request_id
            JOIN User u1 ON rr.customer_id = u1.user_id
            JOIN Technician t ON sa.technician_id = t.technician_id
            JOIN User u2 ON t.user_id = u2.user_id
            WHERE sa.assignment_status = 'completed'
            AND sa.assignment_id NOT IN (SELECT assignment_id FROM Review)
            ORDER BY sa.actual_completion_date DESC
        """)
        
        if assignments:
            with st.form("add_review_form"):
                assignment_options = {
                    f"Assignment #{asg['assignment_id']} - Customer: {asg['customer_first_name']} {asg['customer_last_name']} | Tech: {asg['tech_first_name']} {asg['tech_last_name']}": 
                    asg['assignment_id'] for asg in assignments
                }
                selected_assignment = st.selectbox("Select Assignment *", options=list(assignment_options.keys()))
                assignment_id = assignment_options[selected_assignment]
                
                col1, col2 = st.columns(2)
                with col1:
                    customer_rating = st.slider("Customer Rating *", min_value=1, max_value=5, value=4)
                with col2:
                    technician_rating = st.slider("Technician Rating *", min_value=1, max_value=5, value=4)
                
                review_text = st.text_area("Review Text")
                
                submitted = st.form_submit_button("Add Review")
                if submitted:
                    query = """INSERT INTO Review (assignment_id, customer_rating, technician_rating, 
                               review_text, review_date) VALUES (%s, %s, %s, %s, %s)"""
                    if execute_query(query, (assignment_id, customer_rating, technician_rating, 
                                           review_text, datetime.now()), fetch=False):
                        st.success("Review added successfully!")
                        st.rerun()
        else:
            st.info("No completed assignments available for review")
    
    with tab3:
        st.subheader("Review Analytics")
        
        # Average ratings by technician
        tech_ratings = execute_query("""
            SELECT t.technician_id, u.first_name, u.last_name,
                   AVG(r.technician_rating) as avg_rating, COUNT(r.review_id) as review_count
            FROM Technician t
            JOIN User u ON t.user_id = u.user_id
            JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
            JOIN Review r ON sa.assignment_id = r.assignment_id
            GROUP BY t.technician_id, u.first_name, u.last_name
            HAVING review_count > 0
            ORDER BY avg_rating DESC
        """)
        
        if tech_ratings:
            st.markdown("**Technician Ratings**")
            df_ratings = pd.DataFrame(tech_ratings)
            df_ratings['technician'] = df_ratings['first_name'] + ' ' + df_ratings['last_name']
            
            fig = px.bar(df_ratings, x='technician', y='avg_rating',
                        title="Average Rating by Technician",
                        color='avg_rating', color_continuous_scale='RdYlGn')
            fig.update_layout(xaxis_title="Technician", yaxis_title="Average Rating")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df_ratings[['technician', 'avg_rating', 'review_count']], use_container_width=True)
        
        # Rating distribution
        rating_dist = execute_query("""
            SELECT customer_rating as rating, COUNT(*) as count
            FROM Review
            GROUP BY customer_rating
            ORDER BY customer_rating
        """)
        
        if rating_dist:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Rating Distribution**")
                df_dist = pd.DataFrame(rating_dist)
                fig = px.bar(df_dist, x='rating', y='count',
                           title="Distribution of Ratings")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                avg_rating = execute_query("SELECT AVG(customer_rating) as avg FROM Review")[0]['avg']
                total_reviews = execute_query("SELECT COUNT(*) as count FROM Review")[0]['count']
                
                st.metric("Average Customer Rating", f"{avg_rating:.2f} / 5.0" if avg_rating else "N/A")
                st.metric("Total Reviews", total_reviews)

# ==================== DATABASE FEATURES (NEW SECTION) ====================
def database_features():
    st.title("Database Features Demonstration")
    st.markdown("### Showcasing Procedures, Functions, Triggers, and Views")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Stored Procedures", "Functions", "Triggers", "Views"])
    
    # ========== TAB 1: STORED PROCEDURES ==========
    with tab1:
        st.subheader("Stored Procedures Implementation")
        
        # Procedure 1: AssignTechnicianToRequest
        with st.expander("Procedure 1: AssignTechnicianToRequest", expanded=True):
            st.code("""
PROCEDURE AssignTechnicianToRequest(
    IN p_request_id INT,
    IN p_technician_id INT,
    IN p_service_cost DECIMAL(8,2)
)
-- Automatically:
-- 1. Creates Service Assignment
-- 2. Updates Repair Request status to 'assigned'
-- 3. Updates Technician status to 'busy'
            """, language="sql")
            
            st.markdown("**Test this Procedure:**")
            
            # Get pending requests
            pending_requests = execute_query("""
                SELECT rr.request_id, rr.item_description, u.first_name, u.last_name, 
                       sc.category_name, rr.status
                FROM Repair_Request rr
                JOIN User u ON rr.customer_id = u.user_id
                JOIN Service_Category sc ON rr.category_id = sc.category_id
                WHERE rr.status = 'pending'
                AND rr.request_id NOT IN (SELECT request_id FROM Service_Assignment)
                ORDER BY rr.request_date DESC
                LIMIT 10
            """)
            
            # Get available technicians
            available_techs = execute_query("""
                SELECT t.technician_id, u.first_name, u.last_name, t.experience_years
                FROM Technician t
                JOIN User u ON t.user_id = u.user_id
                WHERE t.availability_status = 'available'
            """)
            
            if pending_requests and available_techs:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    request_options = {
                        f"Req #{req['request_id']} - {req['first_name']} {req['last_name']}": 
                        req['request_id'] for req in pending_requests
                    }
                    selected_request = st.selectbox("Select Request", options=list(request_options.keys()), key="proc1_req")
                    request_id = request_options[selected_request]
                
                with col2:
                    tech_options = {
                        f"Tech #{tech['technician_id']} - {tech['first_name']} {tech['last_name']}": 
                        tech['technician_id'] for tech in available_techs
                    }
                    selected_tech = st.selectbox("Select Technician", options=list(tech_options.keys()), key="proc1_tech")
                    technician_id = tech_options[selected_tech]
                
                with col3:
                    service_cost = st.number_input("Service Cost (₹)", min_value=100.0, value=1500.0, step=100.0, key="proc1_cost")
                
                if st.button("Execute Procedure", key="proc1_btn", type="primary"):
                    conn = get_database_connection()
                    try:
                        cursor = conn.cursor()
                        cursor.callproc('AssignTechnicianToRequest', [request_id, technician_id, service_cost])
                        conn.commit()
                        
                        # Fetch results
                        for result in cursor.stored_results():
                            rows = result.fetchall()
                            for row in rows:
                                st.success(f"{row[0]}")
                        
                        cursor.close()
                        conn.close()
                        st.balloons()
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
            else:
                st.info("No pending requests or available technicians to test this procedure.")
        
        st.markdown("---")
        
        # Procedure 2: CompleteServiceAndPayment
        with st.expander("Procedure 2: CompleteServiceAndPayment", expanded=False):
            st.code("""
PROCEDURE CompleteServiceAndPayment(
    IN p_assignment_id INT,
    IN p_payment_method VARCHAR(20),
    IN p_transaction_ref VARCHAR(100)
)
-- Automatically:
-- 1. Marks assignment as completed
-- 2. Creates payment record
-- 3. Updates technician to 'available'
-- 4. Updates repair request to 'completed'
            """, language="sql")
            
            st.markdown("**Test this Procedure:**")
            
            # Get in-progress assignments
            in_progress = execute_query("""
                SELECT sa.assignment_id, rr.item_description, 
                       u1.first_name as customer_name, u2.first_name as tech_name,
                       sa.service_cost, sa.assignment_status
                FROM Service_Assignment sa
                JOIN Repair_Request rr ON sa.request_id = rr.request_id
                JOIN User u1 ON rr.customer_id = u1.user_id
                JOIN Technician t ON sa.technician_id = t.technician_id
                JOIN User u2 ON t.user_id = u2.user_id
                WHERE sa.assignment_status IN ('assigned', 'in_progress')
                AND sa.assignment_id NOT IN (SELECT assignment_id FROM Payment)
                LIMIT 10
            """)
            
            if in_progress:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    assign_options = {
                        f"Assignment #{asg['assignment_id']} - {asg['customer_name']} (₹{asg['service_cost']})": 
                        asg for asg in in_progress
                    }
                    selected_assign = st.selectbox("Select Assignment", options=list(assign_options.keys()), key="proc2_assign")
                    assignment_data = assign_options[selected_assign]
                
                with col2:
                    payment_method = st.selectbox("Payment Method", ["cash", "card", "upi", "wallet"], key="proc2_method")
                
                with col3:
                    transaction_ref = st.text_input("Transaction Ref", value=f"TXN{datetime.now().strftime('%Y%m%d%H%M')}", key="proc2_ref")
                
                if st.button("Execute Procedure", key="proc2_btn", type="primary"):
                    conn = get_database_connection()
                    try:
                        cursor = conn.cursor()
                        cursor.callproc('CompleteServiceAndPayment', 
                                      [assignment_data['assignment_id'], payment_method, transaction_ref])
                        conn.commit()
                        
                        # Fetch results
                        for result in cursor.stored_results():
                            rows = result.fetchall()
                            for row in rows:
                                st.success(f"{row[0]}")
                        
                        cursor.close()
                        conn.close()
                        st.balloons()
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
            else:
                st.info("No active assignments available to test this procedure.")
        
        st.markdown("---")
        
        # Procedure 3: GetTechnicianDashboard
        with st.expander("Procedure 3: GetTechnicianDashboard", expanded=False):
            st.code("""
PROCEDURE GetTechnicianDashboard(IN p_technician_id INT)
-- Returns:
-- 1. Technician basic info with rating
-- 2. Earnings summary
-- 3. Recent 10 assignments
            """, language="sql")
            
            st.markdown("**Test this Procedure:**")
            
            # Get all technicians
            technicians = execute_query("""
                SELECT t.technician_id, u.first_name, u.last_name
                FROM Technician t
                JOIN User u ON t.user_id = u.user_id
            """)
            
            if technicians:
                tech_options = {
                    f"Technician #{tech['technician_id']} - {tech['first_name']} {tech['last_name']}": 
                    tech['technician_id'] for tech in technicians
                }
                selected_tech = st.selectbox("Select Technician", options=list(tech_options.keys()), key="proc3_tech")
                tech_id = tech_options[selected_tech]
                
                if st.button("Execute Procedure", key="proc3_btn", type="primary"):
                    conn = get_database_connection()
                    try:
                        cursor = conn.cursor(dictionary=True)
                        cursor.callproc('GetTechnicianDashboard', [tech_id])
                        
                        result_num = 0
                        for result in cursor.stored_results():
                            result_num += 1
                            rows = result.fetchall()
                            
                            if result_num == 1:
                                st.markdown("**Basic Info:**")
                                df = pd.DataFrame(rows)
                                st.dataframe(df, use_container_width=True)
                            elif result_num == 2:
                                st.markdown("**Earnings Summary:**")
                                df = pd.DataFrame(rows)
                                st.dataframe(df, use_container_width=True)
                            elif result_num == 3:
                                st.markdown("**Recent Assignments:**")
                                df = pd.DataFrame(rows)
                                st.dataframe(df, use_container_width=True)
                        
                        cursor.close()
                        conn.close()
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
    
    # ========== TAB 2: FUNCTIONS ==========
    with tab2:
        st.subheader("User-Defined Functions")
        
        # Function 1: GetTechnicianRating
        with st.expander("Function 1: GetTechnicianRating", expanded=True):
            st.code("""
FUNCTION GetTechnicianRating(p_technician_id INT) 
RETURNS DECIMAL(3,2)
-- Calculates average rating for a technician
            """, language="sql")
            
            st.markdown("**Test this Function:**")
            
            technicians = execute_query("""
                SELECT t.technician_id, u.first_name, u.last_name
                FROM Technician t
                JOIN User u ON t.user_id = u.user_id
            """)
            
            if technicians:
                tech_options = {
                    f"Tech #{tech['technician_id']} - {tech['first_name']} {tech['last_name']}": 
                    tech['technician_id'] for tech in technicians
                }
                selected_tech = st.selectbox("Select Technician", options=list(tech_options.keys()), key="func1_tech")
                tech_id = tech_options[selected_tech]
                
                if st.button("Execute Function", key="func1_btn", type="primary"):
                    result = execute_query(f"SELECT GetTechnicianRating({tech_id}) as rating")
                    if result:
                        rating = result[0]['rating']
                        st.success(f"Technician Rating: **{rating:.2f} / 5.0**")
                        
                        # Show rating visualization
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=float(rating),
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Rating"},
                            gauge={'axis': {'range': [None, 5]},
                                   'bar': {'color': "darkblue"},
                                   'steps': [
                                       {'range': [0, 2], 'color': "lightgray"},
                                       {'range': [2, 3.5], 'color': "gray"},
                                       {'range': [3.5, 5], 'color': "lightgreen"}],
                                   'threshold': {'line': {'color': "red", 'width': 4}, 
                                               'thickness': 0.75, 'value': 4}}))
                        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Function 2: GetTechnicianEarnings
        with st.expander("Function 2: GetTechnicianEarnings", expanded=False):
            st.code("""
FUNCTION GetTechnicianEarnings(
    p_technician_id INT, 
    p_start_date DATE, 
    p_end_date DATE
) RETURNS DECIMAL(10,2)
-- Calculates total earnings in a date range
            """, language="sql")
            
            st.markdown("**Test this Function:**")
            
            if technicians:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    selected_tech2 = st.selectbox("Select Technician", options=list(tech_options.keys()), key="func2_tech")
                    tech_id2 = tech_options[selected_tech2]
                
                with col2:
                    start_date = st.date_input("Start Date", value=date(2024, 1, 1), key="func2_start")
                
                with col3:
                    end_date = st.date_input("End Date", value=date.today(), key="func2_end")
                
                if st.button("Execute Function", key="func2_btn", type="primary"):
                    result = execute_query(
                        f"SELECT GetTechnicianEarnings({tech_id2}, '{start_date}', '{end_date}') as earnings"
                    )
                    if result:
                        earnings = result[0]['earnings']
                        st.success(f"Total Earnings: **₹{earnings:,.2f}**")
                        st.info(f"Period: {start_date} to {end_date}")
    
    # ========== TAB 3: TRIGGERS ==========
    with tab3:
        st.subheader("Database Triggers")
        st.info("Triggers execute automatically on INSERT, UPDATE, or DELETE operations")
        
        # Trigger 1
        with st.expander("Trigger 1: after_assignment_insert", expanded=True):
            st.code("""
CREATE TRIGGER after_assignment_insert
AFTER INSERT ON Service_Assignment
FOR EACH ROW
-- Automatically updates Repair_Request status to 'assigned'
-- when a new assignment is created
            """, language="sql")
            
            st.markdown("**How it works:**")
            st.markdown("""
            1. When you create a Service Assignment
            2. The trigger **automatically** updates the corresponding Repair Request
            3. Sets the request status to 'assigned'
            """)
            
            # Show recent trigger activations
            recent = execute_query("""
                SELECT sa.assignment_id, sa.assignment_date, rr.request_id, 
                       rr.status, u.first_name, u.last_name
                FROM Service_Assignment sa
                JOIN Repair_Request rr ON sa.request_id = rr.request_id
                JOIN User u ON rr.customer_id = u.user_id
                ORDER BY sa.assignment_date DESC
                LIMIT 5
            """)
            
            if recent:
                st.markdown("**Recent Trigger Activations:**")
                df = pd.DataFrame(recent)
                st.dataframe(df, use_container_width=True)
                st.caption("All these requests were automatically updated to 'assigned' status by the trigger")
        
        st.markdown("---")
        
        # Trigger 2
        with st.expander("Trigger 2: before_technician_delete", expanded=False):
            st.code("""
CREATE TRIGGER before_technician_delete
BEFORE DELETE ON Technician
FOR EACH ROW
-- Prevents deletion of technicians with active assignments
-- Throws error if technician has 'assigned' or 'in_progress' jobs
            """, language="sql")
            
            st.markdown("**How it works:**")
            st.markdown("""
            1. Before deleting a technician
            2. Trigger checks for active assignments
            3. If active jobs exist, **deletion is blocked** with error message
            4. Protects data integrity
            """)
            
            # Show technicians with active assignments
            active = execute_query("""
                SELECT t.technician_id, u.first_name, u.last_name,
                       COUNT(sa.assignment_id) as active_assignments
                FROM Technician t
                JOIN User u ON t.user_id = u.user_id
                LEFT JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
                    AND sa.assignment_status IN ('assigned', 'in_progress')
                GROUP BY t.technician_id, u.first_name, u.last_name
                HAVING active_assignments > 0
            """)
            
            if active:
                st.markdown("**Protected Technicians (Cannot be deleted):**")
                df = pd.DataFrame(active)
                st.dataframe(df, use_container_width=True)
                st.warning("These technicians have active assignments and are protected by the trigger")
            else:
                st.success("Currently no technicians with active assignments")
        
        st.markdown("---")
        
        # Trigger 3
        with st.expander("Trigger 3: before_payment_insert", expanded=False):
            st.code("""
CREATE TRIGGER before_payment_insert
BEFORE INSERT ON Payment
FOR EACH ROW
-- Validates payment amount matches service cost
-- Prevents incorrect payment amounts
            """, language="sql")
            
            st.markdown("**How it works:**")
            st.markdown("""
            1. Before inserting a payment record
            2. Trigger checks if payment_amount matches service_cost
            3. If amounts don't match, **insertion is blocked**
            4. Ensures payment accuracy
            """)
            
            # Show payment validation examples
            validations = execute_query("""
                SELECT p.payment_id, p.payment_amount, sa.service_cost,
                       CASE 
                           WHEN p.payment_amount = sa.service_cost THEN 'Valid'
                           ELSE 'Invalid'
                       END as validation_status
                FROM Payment p
                JOIN Service_Assignment sa ON p.assignment_id = sa.assignment_id
                ORDER BY p.payment_date DESC
                LIMIT 10
            """)
            
            if validations:
                st.markdown("**Recent Payment Validations:**")
                df = pd.DataFrame(validations)
                st.dataframe(df, use_container_width=True)
                st.caption("All payments passed trigger validation")
    
    # ========== TAB 4: VIEWS ==========
    with tab4:
        st.subheader("Database Views")
        st.info("Views are virtual tables that simplify complex queries")
        
        view_choice = st.selectbox("Select a View to Display", [
            "Technician_Rating_View",
            "Popular_Categories_View", 
            "Customer_Service_History",
            "Technician_Earnings_View",
            "Pending_Requests_By_Location"
        ])
        
        if view_choice == "Technician_Rating_View":
            st.markdown("**Technician Rating View**")
            st.code("""
VIEW: Shows technician ratings with review counts and completed jobs
            """, language="sql")
            data = execute_query("SELECT * FROM Technician_Rating_View ORDER BY rating_average DESC")
            
        elif view_choice == "Popular_Categories_View":
            st.markdown("**Popular Categories View**")
            st.code("""
VIEW: Shows service categories ranked by request count and average rating
            """, language="sql")
            data = execute_query("SELECT * FROM Popular_Categories_View")
            
        elif view_choice == "Customer_Service_History":
            st.markdown("**Customer Service History**")
            st.code("""
VIEW: Shows customer request history and total spending
            """, language="sql")
            data = execute_query("SELECT * FROM Customer_Service_History ORDER BY total_spent DESC")
            
        elif view_choice == "Technician_Earnings_View":
            st.markdown("**Technician Earnings View**")
            st.code("""
VIEW: Shows technician job counts and earnings summary
            """, language="sql")
            data = execute_query("SELECT * FROM Technician_Earnings_View ORDER BY total_earnings DESC")
            
        else:  # Pending_Requests_By_Location
            st.markdown("**Pending Requests By Location**")
            st.code("""
VIEW: Shows pending request count grouped by location
            """, language="sql")
            data = execute_query("SELECT * FROM Pending_Requests_By_Location")
        
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Add visualization
            if view_choice == "Technician_Rating_View" and len(df) > 0:
                fig = px.bar(df, x='first_name', y='rating_average', 
                           title="Technician Ratings Comparison",
                           labels={'first_name': 'Technician', 'rating_average': 'Rating'})
                st.plotly_chart(fig, use_container_width=True)
            
            elif view_choice == "Popular_Categories_View" and len(df) > 0:
                fig = px.pie(df, values='total_requests', names='category_name',
                           title="Service Category Distribution")
                st.plotly_chart(fig, use_container_width=True)

# ==================== ADVANCED OPERATIONS ====================
def advanced_operations():
    st.title("Advanced Operations")
    
    tab1, tab2 = st.tabs(["Complex Queries", "Reports"])
    
    with tab1:
        st.subheader("Complex Queries & Analytics")
        
        # Top Performing Technicians
        st.markdown("**Top Performing Technicians (by revenue & rating)**")
        top_techs = execute_query("""
            SELECT t.technician_id, u.first_name, u.last_name,
                   COUNT(DISTINCT sa.assignment_id) as total_jobs,
                   SUM(p.payment_amount) as total_revenue,
                   AVG(r.technician_rating) as avg_rating
            FROM Technician t
            JOIN User u ON t.user_id = u.user_id
            JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
            LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id AND p.payment_status = 'completed'
            LEFT JOIN Review r ON sa.assignment_id = r.assignment_id
            WHERE sa.assignment_status = 'completed'
            GROUP BY t.technician_id, u.first_name, u.last_name
            HAVING total_revenue IS NOT NULL
            ORDER BY total_revenue DESC, avg_rating DESC
            LIMIT 10
        """)
        if top_techs:
            df_top = pd.DataFrame(top_techs)
            st.dataframe(df_top, use_container_width=True)
        
        st.markdown("---")
        
        # Most Requested Service Categories
        st.markdown("**Most Requested Service Categories**")
        category_stats = execute_query("""
            SELECT sc.category_name,
                   COUNT(rr.request_id) as total_requests,
                   SUM(CASE WHEN rr.status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN rr.status = 'pending' THEN 1 ELSE 0 END) as pending,
                   AVG(p.payment_amount) as avg_payment
            FROM Service_Category sc
            LEFT JOIN Repair_Request rr ON sc.category_id = rr.category_id
            LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
            LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id AND p.payment_status = 'completed'
            GROUP BY sc.category_id, sc.category_name
            ORDER BY total_requests DESC
        """)
        if category_stats:
            df_cat = pd.DataFrame(category_stats)
            st.dataframe(df_cat, use_container_width=True)
        
        st.markdown("---")
        
        # Location-wise Analysis
        st.markdown("**Location-wise Service Analysis**")
        location_stats = execute_query("""
            SELECT l.area_name, l.city, l.state,
                   COUNT(DISTINCT rr.request_id) as total_requests,
                   COUNT(DISTINCT t.technician_id) as technicians_in_area,
                   SUM(p.payment_amount) as total_revenue
            FROM Location l
            LEFT JOIN User u ON l.location_id = u.location_id
            LEFT JOIN Repair_Request rr ON u.user_id = rr.customer_id
            LEFT JOIN Technician t ON l.location_id = (SELECT location_id FROM User WHERE user_id = t.user_id)
            LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
            LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id AND p.payment_status = 'completed'
            GROUP BY l.location_id, l.area_name, l.city, l.state
            ORDER BY total_revenue DESC
        """)
        if location_stats:
            df_loc = pd.DataFrame(location_stats)
            st.dataframe(df_loc, use_container_width=True)
    
    with tab2:
        st.subheader("Reports")
        
        report_type = st.selectbox("Select Report Type", 
                                   ["Service Completion Report", 
                                    "Technician Performance Report",
                                    "Revenue Analysis Report",
                                    "Customer Satisfaction Report"])
        
        if st.button("Generate Report"):
            if report_type == "Service Completion Report":
                data = execute_query("""
                    SELECT rr.request_id, u.first_name, u.last_name, sc.category_name,
                           rr.status, rr.request_date, sa.actual_completion_date,
                           DATEDIFF(sa.actual_completion_date, rr.request_date) as days_to_complete
                    FROM Repair_Request rr
                    JOIN User u ON rr.customer_id = u.user_id
                    JOIN Service_Category sc ON rr.category_id = sc.category_id
                    LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
                    WHERE rr.status = 'completed'
                    ORDER BY rr.request_date DESC
                """)
                
            elif report_type == "Technician Performance Report":
                data = execute_query("""
                    SELECT t.technician_id, u.first_name, u.last_name,
                           COUNT(sa.assignment_id) as total_assignments,
                           SUM(CASE WHEN sa.assignment_status = 'completed' THEN 1 ELSE 0 END) as completed,
                           AVG(r.technician_rating) as avg_rating,
                           SUM(p.payment_amount) as total_earnings
                    FROM Technician t
                    JOIN User u ON t.user_id = u.user_id
                    LEFT JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
                    LEFT JOIN Review r ON sa.assignment_id = r.assignment_id
                    LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id AND p.payment_status = 'completed'
                    GROUP BY t.technician_id, u.first_name, u.last_name
                    ORDER BY total_earnings DESC
                """)
                
            elif report_type == "Revenue Analysis Report":
                data = execute_query("""
                    SELECT DATE_FORMAT(p.payment_date, '%%Y-%%m') as month,
                           sc.category_name,
                           COUNT(p.payment_id) as transaction_count,
                           SUM(p.payment_amount) as total_revenue,
                           AVG(p.payment_amount) as avg_transaction
                    FROM Payment p
                    JOIN Service_Assignment sa ON p.assignment_id = sa.assignment_id
                    JOIN Repair_Request rr ON sa.request_id = rr.request_id
                    JOIN Service_Category sc ON rr.category_id = sc.category_id
                    WHERE p.payment_status = 'completed'
                    GROUP BY month, sc.category_name
                    ORDER BY month DESC, total_revenue DESC
                """)
                
            else:  # Customer Satisfaction Report
                data = execute_query("""
                    SELECT u.user_id, u.first_name, u.last_name,
                           COUNT(rr.request_id) as total_requests,
                           AVG(r.customer_rating) as avg_rating_given,
                           SUM(p.payment_amount) as total_spent
                    FROM User u
                    LEFT JOIN Repair_Request rr ON u.user_id = rr.customer_id
                    LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
                    LEFT JOIN Review r ON sa.assignment_id = r.assignment_id
                    LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id AND p.payment_status = 'completed'
                    WHERE u.user_type = 'customer'
                    GROUP BY u.user_id, u.first_name, u.last_name
                    HAVING total_requests > 0
                    ORDER BY avg_rating_given DESC
                """)
            
            if data:
                df_report = pd.DataFrame(data)
                st.dataframe(df_report, use_container_width=True)
                
                # Download option
                csv = df_report.to_csv(index=False)
                st.download_button(
                    label="Download Report as CSV",
                    data=csv,
                    file_name=f"{report_type.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

# ==================== MAIN APP ====================
def main():
    # Sidebar navigation
    st.sidebar.title("Repair Service System")
    st.sidebar.markdown("---")
    
    menu_options = {
        "Dashboard": dashboard_page,
        "Locations": location_management,
        "Users": user_management,
        "Technicians": technician_management,
        "Service Categories": service_category_management,
        "Repair Requests": repair_request_management,
        "Service Assignments": service_assignment,
        "Payments": payment_management,
        "Reviews": review_management,
        "Database Features": database_features,
        "Advanced Operations": advanced_operations
    }
    
    choice = st.sidebar.radio("Navigation", list(menu_options.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Repair Service Management System**
    
    A comprehensive system for managing local repair services with:
    - User & Technician Management
    - Service Request Tracking
    - Payment Processing
    - Review System
    - Analytics & Reports
    """)
    
    # Call selected page function
    menu_options[choice]()

if __name__ == "__main__":
    main()