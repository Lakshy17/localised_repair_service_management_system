-- DATABASE CREATION
CREATE DATABASE IF NOT EXISTS repair_service_db;
USE repair_service_db;

-- ============================================
-- TABLE 1: LOCATION (Strong Entity)
-- ============================================
CREATE TABLE Location (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    area_name VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    service_availability BOOLEAN DEFAULT TRUE,
    delivery_charge DECIMAL(8,2) DEFAULT 0.00
);

-- Insert 20 Location records
INSERT INTO Location (area_name, pincode, city, state, service_availability, delivery_charge) VALUES
('Koramangala', '560034', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Indiranagar', '560038', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Whitefield', '560066', 'Bangalore', 'Karnataka', TRUE, 100.00),
('Jayanagar', '560041', 'Bangalore', 'Karnataka', TRUE, 50.00),
('HSR Layout', '560102', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Marathahalli', '560037', 'Bangalore', 'Karnataka', TRUE, 75.00),
('Electronic City', '560100', 'Bangalore', 'Karnataka', TRUE, 100.00),
('BTM Layout', '560076', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Malleshwaram', '560003', 'Bangalore', 'Karnataka', TRUE, 60.00),
('Rajajinagar', '560010', 'Bangalore', 'Karnataka', TRUE, 60.00),
('JP Nagar', '560078', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Banashankari', '560070', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Yelahanka', '560064', 'Bangalore', 'Karnataka', TRUE, 100.00),
('Hebbal', '560024', 'Bangalore', 'Karnataka', TRUE, 80.00),
('MG Road', '560001', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Brigade Road', '560025', 'Bangalore', 'Karnataka', TRUE, 50.00),
('Basavanagudi', '560004', 'Bangalore', 'Karnataka', TRUE, 50.00),
('RT Nagar', '560032', 'Bangalore', 'Karnataka', TRUE, 70.00),
('Bellandur', '560103', 'Bangalore', 'Karnataka', TRUE, 80.00),
('Sarjapur Road', '560035', 'Bangalore', 'Karnataka', TRUE, 90.00);

-- ============================================
-- TABLE 2: USER (Strong Entity)
-- ============================================
CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    registration_date DATE NOT NULL,
    user_type ENUM('customer', 'technician') NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Location(location_id) ON DELETE RESTRICT
);

-- Insert 25 User records (mix of customers and technicians)
INSERT INTO User (first_name, last_name, email, phone_number, street, city, state, pincode, registration_date, user_type, location_id) VALUES
('Rahul', 'Sharma', 'rahul.sharma@email.com', '9876543210', '123 MG Road', 'Bangalore', 'Karnataka', '560001', '2024-01-15', 'customer', 15),
('Priya', 'Patel', 'priya.patel@email.com', '9876543211', '45 Koramangala', 'Bangalore', 'Karnataka', '560034', '2024-01-20', 'technician', 1),
('Amit', 'Kumar', 'amit.kumar@email.com', '9876543212', '67 Indiranagar', 'Bangalore', 'Karnataka', '560038', '2024-02-01', 'customer', 2),
('Sneha', 'Reddy', 'sneha.reddy@email.com', '9876543213', '89 Whitefield', 'Bangalore', 'Karnataka', '560066', '2024-02-05', 'technician', 3),
('Vikram', 'Singh', 'vikram.singh@email.com', '9876543214', '12 Jayanagar', 'Bangalore', 'Karnataka', '560041', '2024-02-10', 'customer', 4),
('Ananya', 'Iyer', 'ananya.iyer@email.com', '9876543215', '34 HSR Layout', 'Bangalore', 'Karnataka', '560102', '2024-02-15', 'technician', 5),
('Karthik', 'Menon', 'karthik.menon@email.com', '9876543216', '56 Marathahalli', 'Bangalore', 'Karnataka', '560037', '2024-02-20', 'customer', 6),
('Divya', 'Nair', 'divya.nair@email.com', '9876543217', '78 Electronic City', 'Bangalore', 'Karnataka', '560100', '2024-03-01', 'technician', 7),
('Rohan', 'Gupta', 'rohan.gupta@email.com', '9876543218', '90 BTM Layout', 'Bangalore', 'Karnataka', '560076', '2024-03-05', 'customer', 8),
('Pooja', 'Desai', 'pooja.desai@email.com', '9876543219', '11 Malleshwaram', 'Bangalore', 'Karnataka', '560003', '2024-03-10', 'technician', 9),
('Arjun', 'Rao', 'arjun.rao@email.com', '9876543220', '22 Rajajinagar', 'Bangalore', 'Karnataka', '560010', '2024-03-15', 'customer', 10),
('Lakshmi', 'Krishnan', 'lakshmi.k@email.com', '9876543221', '33 JP Nagar', 'Bangalore', 'Karnataka', '560078', '2024-03-20', 'technician', 11),
('Suresh', 'Pillai', 'suresh.pillai@email.com', '9876543222', '44 Banashankari', 'Bangalore', 'Karnataka', '560070', '2024-04-01', 'customer', 12),
('Meera', 'Joshi', 'meera.joshi@email.com', '9876543223', '55 Yelahanka', 'Bangalore', 'Karnataka', '560064', '2024-04-05', 'technician', 13),
('Naveen', 'Agarwal', 'naveen.agarwal@email.com', '9876543224', '66 Hebbal', 'Bangalore', 'Karnataka', '560024', '2024-04-10', 'customer', 14),
('Kavya', 'Verma', 'kavya.verma@email.com', '9876543225', '77 Brigade Road', 'Bangalore', 'Karnataka', '560025', '2024-04-15', 'technician', 16),
('Aditya', 'Chopra', 'aditya.chopra@email.com', '9876543226', '88 Basavanagudi', 'Bangalore', 'Karnataka', '560004', '2024-04-20', 'customer', 17),
('Nisha', 'Kapoor', 'nisha.kapoor@email.com', '9876543227', '99 RT Nagar', 'Bangalore', 'Karnataka', '560032', '2024-05-01', 'technician', 18),
('Sanjay', 'Malhotra', 'sanjay.malhotra@email.com', '9876543228', '101 Bellandur', 'Bangalore', 'Karnataka', '560103', '2024-05-05', 'customer', 19),
('Ritu', 'Saxena', 'ritu.saxena@email.com', '9876543229', '102 Sarjapur Road', 'Bangalore', 'Karnataka', '560035', '2024-05-10', 'technician', 20),
('Manish', 'Tiwari', 'manish.tiwari@email.com', '9876543230', '103 Koramangala', 'Bangalore', 'Karnataka', '560034', '2024-05-15', 'customer', 1),
('Swati', 'Bhatt', 'swati.bhatt@email.com', '9876543231', '104 Indiranagar', 'Bangalore', 'Karnataka', '560038', '2024-05-20', 'customer', 2),
('Rajesh', 'Sinha', 'rajesh.sinha@email.com', '9876543232', '105 HSR Layout', 'Bangalore', 'Karnataka', '560102', '2024-06-01', 'customer', 5),
('Deepa', 'Mehta', 'deepa.mehta@email.com', '9876543233', '106 Jayanagar', 'Bangalore', 'Karnataka', '560041', '2024-06-05', 'customer', 4),
('Varun', 'Kohli', 'varun.kohli@email.com', '9876543234', '107 Whitefield', 'Bangalore', 'Karnataka', '560066', '2024-06-10', 'customer', 3);

-- ============================================
-- TABLE 3: TECHNICIAN (Weak Entity)
-- ============================================
CREATE TABLE Technician (
    technician_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    experience_years INT NOT NULL,
    certification_details TEXT,
    availability_status ENUM('available', 'busy', 'offline') DEFAULT 'available',
    created_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Insert 10 Technician records (for users who are technicians)
INSERT INTO Technician (user_id, experience_years, certification_details, availability_status, created_date) VALUES
(2, 5, 'Certified Electronics Repair Technician - IIT Delhi', 'available', '2024-01-20'),
(4, 3, 'Mobile Phone Repair Certification - Samsung', 'available', '2024-02-05'),
(6, 7, 'Laptop & Computer Hardware Specialist - HP Certified', 'busy', '2024-02-15'),
(8, 4, 'Furniture Restoration Expert - National Institute', 'available', '2024-03-01'),
(10, 6, 'Clothing Alteration Master - Fashion Institute', 'available', '2024-03-10'),
(12, 8, 'Electronics & Appliance Repair - Whirlpool Certified', 'available', '2024-03-20'),
(14, 2, 'Smartphone Repair Specialist - Apple Authorized', 'offline', '2024-04-05'),
(16, 5, 'Textile & Clothing Repair Professional', 'available', '2024-04-15'),
(18, 4, 'Furniture Upholstery & Repair Expert', 'available', '2024-05-01'),
(20, 3, 'General Electronics & Gadget Repair', 'available', '2024-05-10');

-- ============================================
-- TABLE 4: TECHNICIAN_SPECIALIZATION (Normalized Multi-valued Attribute)
-- ============================================
CREATE TABLE Technician_Specialization (
    tech_spec_id INT PRIMARY KEY AUTO_INCREMENT,
    technician_id INT NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    FOREIGN KEY (technician_id) REFERENCES Technician(technician_id) ON DELETE CASCADE
);

-- Insert specializations for technicians (multiple per technician)
INSERT INTO Technician_Specialization (technician_id, specialization) VALUES
(1, 'Smartphone Repair'),
(1, 'Laptop Repair'),
(1, 'Tablet Repair'),
(2, 'Smartphone Repair'),
(2, 'Mobile Accessories'),
(3, 'Laptop Repair'),
(3, 'Desktop Repair'),
(3, 'Gaming Console Repair'),
(4, 'Furniture Repair'),
(4, 'Furniture Restoration'),
(4, 'Wood Polishing'),
(5, 'Clothing Alteration'),
(5, 'Tailoring'),
(5, 'Embroidery'),
(6, 'TV Repair'),
(6, 'Refrigerator Repair'),
(6, 'Washing Machine Repair'),
(7, 'iPhone Repair'),
(7, 'MacBook Repair'),
(8, 'Clothing Alteration'),
(8, 'Dress Making'),
(9, 'Sofa Repair'),
(9, 'Chair Upholstery'),
(10, 'Smartwatch Repair'),
(10, 'Headphone Repair');

-- ============================================
-- TABLE 5: SERVICE_CATEGORY (Strong Entity)
-- ============================================
CREATE TABLE Service_Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL,
    category_description TEXT,
    base_service_charge DECIMAL(8,2) NOT NULL,
    estimated_time_hours INT NOT NULL,
    popularity_score DECIMAL(3,2) DEFAULT 0.00
);

-- Insert 20 Service Categories
INSERT INTO Service_Category (category_name, category_description, base_service_charge, estimated_time_hours, popularity_score) VALUES
('Smartphone Screen Repair', 'Repair cracked or damaged smartphone screens', 1500.00, 2, 4.5),
('Laptop Hardware Repair', 'Fix laptop hardware issues including motherboard, RAM, etc.', 2500.00, 4, 4.3),
('Clothing Alteration', 'Resize and alter clothing items', 300.00, 1, 4.2),
('Furniture Restoration', 'Restore old furniture to new condition', 3000.00, 8, 4.0),
('Mobile Battery Replacement', 'Replace worn-out mobile phone batteries', 800.00, 1, 4.6),
('Laptop Screen Replacement', 'Replace broken laptop screens', 3500.00, 3, 4.4),
('Sofa Upholstery', 'Re-upholster sofas and couches', 5000.00, 12, 3.9),
('Dress Tailoring', 'Custom tailoring and stitching of dresses', 1000.00, 3, 4.1),
('TV Repair', 'Repair LED/LCD TV issues', 2000.00, 3, 4.0),
('Refrigerator Repair', 'Fix refrigerator cooling and other issues', 1800.00, 2, 4.2),
('Washing Machine Repair', 'Repair washing machine faults', 1500.00, 2, 4.3),
('Chair Repair', 'Fix broken chairs and replace parts', 800.00, 2, 3.8),
('Tablet Repair', 'Repair tablet screens and hardware', 2000.00, 3, 4.0),
('Smartwatch Repair', 'Fix smartwatch display and battery issues', 1200.00, 2, 3.7),
('Gaming Console Repair', 'Repair PlayStation, Xbox, and other consoles', 2500.00, 4, 4.1),
('Curtain Stitching', 'Stitch and alter curtains', 500.00, 2, 3.9),
('Wood Furniture Polishing', 'Polish and refinish wooden furniture', 2000.00, 6, 4.0),
('Headphone Repair', 'Fix headphone wiring and audio issues', 500.00, 1, 3.6),
('Desktop PC Repair', 'Repair desktop computer hardware', 1800.00, 3, 4.2),
('Blouse Stitching', 'Custom blouse stitching and fitting', 600.00, 2, 4.3);

-- ============================================
-- TABLE 6: REPAIR_REQUEST (Strong Entity)
-- ============================================
CREATE TABLE Repair_Request (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    category_id INT NOT NULL,
    item_description TEXT NOT NULL,
    issue_description TEXT NOT NULL,
    priority_level ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    request_date DATETIME NOT NULL,
    preferred_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Service_Category(category_id) ON DELETE RESTRICT
);

-- Insert 25 Repair Requests
INSERT INTO Repair_Request (customer_id, category_id, item_description, issue_description, priority_level, request_date, preferred_date, status) VALUES
(1, 1, 'iPhone 13 Pro', 'Screen cracked after drop', 'high', '2024-06-15 10:30:00', '2024-06-16', 'assigned'),
(3, 2, 'Dell XPS 15', 'Laptop not turning on, possible motherboard issue', 'urgent', '2024-06-16 14:20:00', '2024-06-17', 'assigned'),
(5, 3, 'Blue Jeans', 'Need to shorten length by 2 inches', 'low', '2024-06-17 09:15:00', '2024-06-20', 'completed'),
(7, 4, 'Wooden Dining Table', 'Surface scratched, needs restoration', 'medium', '2024-06-18 11:45:00', '2024-06-25', 'in_progress'),
(9, 5, 'Samsung Galaxy S21', 'Battery draining very fast', 'high', '2024-06-19 16:30:00', '2024-06-20', 'completed'),
(11, 6, 'HP Pavilion', 'Screen has dead pixels and lines', 'high', '2024-06-20 10:00:00', '2024-06-22', 'assigned'),
(13, 7, '3-Seater Sofa', 'Fabric torn, needs re-upholstery', 'medium', '2024-06-21 13:20:00', '2024-07-01', 'pending'),
(15, 8, 'Wedding Dress', 'Need alterations for better fit', 'urgent', '2024-06-22 15:45:00', '2024-06-24', 'in_progress'),
(17, 9, 'Sony Bravia 55 inch', 'Screen flickering issue', 'medium', '2024-06-23 12:10:00', '2024-06-26', 'completed'),
(19, 10, 'LG Double Door Fridge', 'Not cooling properly', 'high', '2024-06-24 09:30:00', '2024-06-25', 'completed'),
(21, 11, 'Samsung Front Load', 'Making loud noise during spin cycle', 'medium', '2024-06-25 14:15:00', '2024-06-27', 'assigned'),
(23, 12, 'Office Chair', 'Broken armrest and wobbly base', 'low', '2024-06-26 11:00:00', '2024-06-30', 'pending'),
(1, 13, 'iPad Air', 'Touch screen not responding', 'high', '2024-06-27 10:20:00', '2024-06-28', 'in_progress'),
(3, 14, 'Apple Watch Series 7', 'Screen cracked and battery issue', 'medium', '2024-06-28 16:40:00', '2024-07-01', 'pending'),
(5, 15, 'PlayStation 5', 'Console overheating and shutting down', 'high', '2024-06-29 13:25:00', '2024-07-02', 'assigned'),
(7, 16, 'Living Room Curtains', 'Need hemming and adjustments', 'low', '2024-06-30 09:50:00', '2024-07-05', 'pending'),
(9, 17, 'Teak Wood Bookshelf', 'Needs polishing and minor repairs', 'medium', '2024-07-01 14:30:00', '2024-07-08', 'pending'),
(11, 18, 'Sony WH-1000XM4', 'One side not working', 'medium', '2024-07-02 11:15:00', '2024-07-04', 'completed'),
(13, 19, 'Gaming Desktop PC', 'Random shutdowns and blue screen errors', 'urgent', '2024-07-03 15:00:00', '2024-07-04', 'in_progress'),
(15, 20, 'Silk Saree Blouse', 'Need custom stitching', 'medium', '2024-07-04 10:45:00', '2024-07-08', 'pending'),
(17, 1, 'OnePlus 11', 'Screen replacement needed', 'high', '2024-07-05 12:30:00', '2024-07-06', 'assigned'),
(19, 2, 'MacBook Pro M2', 'Keyboard keys not working', 'high', '2024-07-06 09:20:00', '2024-07-08', 'pending'),
(21, 3, 'Formal Trousers', 'Waist adjustment needed', 'low', '2024-07-07 14:50:00', '2024-07-12', 'pending'),
(23, 5, 'Xiaomi Redmi Note 12', 'Battery replacement required', 'medium', '2024-07-08 11:35:00', '2024-07-10', 'pending'),
(1, 9, 'Samsung QLED TV', 'No display but audio working', 'urgent', '2024-07-09 16:15:00', '2024-07-10', 'pending');

-- ============================================
-- TABLE 7: SERVICE_ASSIGNMENT (Strong Entity / Associative Entity)
-- ============================================
CREATE TABLE Service_Assignment (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    request_id INT UNIQUE NOT NULL,
    technician_id INT NOT NULL,
    assignment_date DATETIME NOT NULL,
    estimated_completion_date DATE,
    actual_completion_date DATE,
    assignment_status ENUM('assigned', 'in_progress', 'completed', 'cancelled') DEFAULT 'assigned',
    service_cost DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (request_id) REFERENCES Repair_Request(request_id) ON DELETE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES Technician(technician_id) ON DELETE RESTRICT
);

-- Insert 25 Service Assignments
INSERT INTO Service_Assignment (request_id, technician_id, assignment_date, estimated_completion_date, actual_completion_date, assignment_status, service_cost) VALUES
(1, 1, '2024-06-15 11:00:00', '2024-06-16', '2024-06-16', 'completed', 1500.00),
(2, 3, '2024-06-16 15:00:00', '2024-06-18', '2024-06-17', 'completed', 2800.00),
(3, 5, '2024-06-17 10:00:00', '2024-06-20', '2024-06-19', 'completed', 300.00),
(4, 4, '2024-06-18 12:00:00', '2024-06-26', NULL, 'in_progress', 3200.00),
(5, 1, '2024-06-19 17:00:00', '2024-06-20', '2024-06-20', 'completed', 900.00),
(6, 3, '2024-06-20 11:00:00', '2024-06-23', NULL, 'assigned', 3500.00),
(8, 5, '2024-06-22 16:00:00', '2024-06-25', NULL, 'in_progress', 1200.00),
(9, 6, '2024-06-23 13:00:00', '2024-06-26', '2024-06-25', 'completed', 2000.00),
(10, 6, '2024-06-24 10:00:00', '2024-06-25', '2024-06-25', 'completed', 1800.00),
(11, 6, '2024-06-25 15:00:00', '2024-06-27', NULL, 'assigned', 1600.00),
(13, 1, '2024-06-27 11:00:00', '2024-06-29', NULL, 'in_progress', 2200.00),
(15, 3, '2024-06-29 14:00:00', '2024-07-02', NULL, 'assigned', 2600.00),
(18, 10, '2024-07-02 12:00:00', '2024-07-04', '2024-07-03', 'completed', 550.00),
(19, 3, '2024-07-03 16:00:00', '2024-07-05', '2024-07-04', 'completed', 2000.00),
(21, 2, '2024-07-05 13:00:00', '2024-07-07', NULL, 'assigned', 1500.00),
(7, 4, '2024-06-21 14:00:00', '2024-07-01', NULL, 'pending', 5000.00),
(12, 4, '2024-06-26 11:30:00', '2024-06-30', NULL, 'pending', 800.00),
(14, 7, '2024-06-28 17:00:00', '2024-07-01', NULL, 'pending', 1200.00),
(16, 4, '2024-06-30 10:00:00', '2024-07-05', NULL, 'pending', 500.00),
(17, 9, '2024-07-01 15:00:00', '2024-07-08', NULL, 'pending', 2000.00),
(20, 8, '2024-07-04 11:00:00', '2024-07-08', NULL, 'pending', 600.00),
(22, 3, '2024-07-06 09:30:00', '2024-07-08', NULL, 'pending', 3600.00),
(23, 5, '2024-07-07 15:00:00', '2024-07-12', NULL, 'pending', 350.00),
(24, 1, '2024-07-08 12:00:00', '2024-07-10', NULL, 'assigned', 850.00),
(25, 6, '2024-07-09 16:30:00', '2024-07-10', NULL, 'assigned', 2100.00);

-- ============================================
-- TABLE 8: PAYMENT (Strong Entity)
-- ============================================
CREATE TABLE Payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    assignment_id INT UNIQUE NOT NULL,
    payment_amount DECIMAL(8,2) NOT NULL,
    payment_method ENUM('cash', 'card', 'upi', 'wallet') NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_reference VARCHAR(100),
    FOREIGN KEY (assignment_id) REFERENCES Service_Assignment(assignment_id) ON DELETE CASCADE
);

-- Insert 20 Payment records
INSERT INTO Payment (assignment_id, payment_amount, payment_method, payment_date, payment_status, transaction_reference) VALUES
(3, 300.00, 'upi', '2024-06-19 18:30:00', 'completed', 'UPI2406190001'),
(5, 900.00, 'card', '2024-06-20 19:15:00', 'completed', 'CARD2406200002'),
(9, 2000.00, 'upi', '2024-06-25 20:00:00', 'completed', 'UPI2406250003'),
(10, 1800.00, 'wallet', '2024-06-25 21:30:00', 'completed', 'WALLET2406250004'),
(18, 550.00, 'cash', '2024-07-03 15:45:00', 'completed', 'CASH2407030005'),
(1, 1500.00, 'upi', '2024-06-16 14:30:00', 'completed', 'UPI2406160006'),
(2, 2800.00, 'card', '2024-06-17 16:20:00', 'completed', 'CARD2406170007'),
(4, 3200.00, 'upi', '2024-06-26 18:45:00', 'pending', 'UPI2406260008'),
(6, 3500.00, 'card', '2024-06-23 12:30:00', 'pending', 'CARD2406230009'),
(8, 1200.00, 'wallet', '2024-06-25 10:15:00', 'pending', 'WALLET2406250010'),
(11, 1600.00, 'upi', '2024-06-27 17:00:00', 'pending', 'UPI2406270011'),
(13, 2200.00, 'card', '2024-06-29 13:45:00', 'pending', 'CARD2406290012'),
(15, 2600.00, 'upi', '2024-07-02 15:30:00', 'pending', 'UPI2407020013'),
(19, 2000.00, 'wallet', '2024-07-05 11:20:00', 'pending', 'WALLET2407050014'),
(21, 1500.00, 'cash', '2024-07-07 14:00:00', 'pending', 'CASH2407070015'),
(16, 1500.00, 'upi', '2024-06-16 19:00:00', 'completed', 'UPI2406160016'),
(17, 2800.00, 'card', '2024-06-17 20:30:00', 'completed', 'CARD2406170017'),
(18, 900.00, 'upi', '2024-06-20 21:45:00', 'completed', 'UPI2406200018'),
(19, 2000.00, 'wallet', '2024-06-25 22:15:00', 'completed', 'WALLET2406250019'),
(20, 1800.00, 'cash', '2024-06-25 23:00:00', 'completed', 'CASH2406250020');

INSERT INTO Payment (assignment_id, payment_amount, payment_method, payment_date, payment_status, transaction_reference)
SELECT 
    sa.assignment_id,
    sa.service_cost,
    CASE 
        WHEN sa.assignment_id % 4 = 0 THEN 'upi'
        WHEN sa.assignment_id % 4 = 1 THEN 'card'
        WHEN sa.assignment_id % 4 = 2 THEN 'wallet'
        ELSE 'cash'
    END,
    DATE_ADD(sa.assignment_date, INTERVAL 1 DAY),
    CASE 
        WHEN sa.assignment_status = 'completed' THEN 'completed'
        ELSE 'pending'
    END,
    CONCAT(
        CASE 
            WHEN sa.assignment_id % 4 = 0 THEN 'UPI'
            WHEN sa.assignment_id % 4 = 1 THEN 'CARD'
            WHEN sa.assignment_id % 4 = 2 THEN 'WALLET'
            ELSE 'CASH'
        END,
        DATE_FORMAT(sa.assignment_date, '%Y%m%d'),
        LPAD(sa.assignment_id, 4, '0')
    )
FROM Service_Assignment sa
LIMIT 25;

-- ============================================
-- TABLE 9: REVIEW (Weak Entity)
-- ============================================
CREATE TABLE Review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    assignment_id INT UNIQUE NOT NULL,
    customer_rating INT CHECK (customer_rating BETWEEN 1 AND 5),
    technician_rating INT CHECK (technician_rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATETIME NOT NULL,
    helpfulness_score INT DEFAULT 0,
    FOREIGN KEY (assignment_id) REFERENCES Service_Assignment(assignment_id) ON DELETE CASCADE
);

-- Insert 20 Review records
INSERT INTO Review (assignment_id, customer_rating, technician_rating, review_text, review_date, helpfulness_score) VALUES
(3, 5, 5, 'Excellent work! Very professional and quick service.', '2024-06-19 19:00:00', 12),
(5, 4, 5, 'Good service, battery replacement done efficiently.', '2024-06-20 20:00:00', 8),
(9, 5, 5, 'TV working perfectly now. Highly recommended!', '2024-06-25 21:00:00', 15),
(10, 4, 4, 'Fixed the refrigerator issue. Good technician.', '2024-06-25 22:00:00', 10),
(18, 3, 4, 'Headphones repaired but took slightly longer than expected.', '2024-07-03 16:00:00', 5),
(16, 5, 5, 'Amazing service! Screen replaced perfectly on my iPhone.', '2024-06-16 20:00:00', 18),
(17, 4, 5, 'Laptop issue resolved. Technician was very knowledgeable.', '2024-06-17 21:00:00', 14),
(1, 5, 5, 'Quick and efficient screen repair. Very satisfied!', '2024-06-16 15:00:00', 20),
(2, 4, 4, 'Laptop fixed well. Slightly expensive but worth it.', '2024-06-17 17:00:00', 11),
(4, 5, 5, 'Table restoration exceeded expectations. Beautiful work!', '2024-06-26 19:00:00', 16),
(6, 3, 3, 'Service was okay. Screen replacement took longer.', '2024-06-23 13:00:00', 4),
(8, 5, 5, 'Perfect dress alteration! Great attention to detail.', '2024-06-25 11:00:00', 13),
(11, 4, 4, 'Washing machine repair done well. No complaints.', '2024-06-27 18:00:00', 9),
(13, 5, 5, 'Tablet screen replaced perfectly. Excellent technician!', '2024-06-29 14:00:00', 17),
(15, 4, 5, 'PS5 overheating issue fixed. Works great now!', '2024-07-02 16:00:00', 12),
(19, 5, 5, 'Desktop PC running smoothly after repair. Highly satisfied!', '2024-07-05 12:00:00', 19),
(21, 4, 4, 'OnePlus screen replaced well. Good service overall.', '2024-07-07 15:00:00', 10),
(7, 3, 3, 'Sofa upholstery decent but not as expected.', '2024-07-01 14:00:00', 6),
(12, 4, 4, 'Chair repair done properly. Satisfied with work.', '2024-06-30 12:00:00', 8),
(14, 5, 5, 'Apple Watch screen and battery fixed perfectly!', '2024-07-01 15:30:00', 15);

INSERT INTO Review (assignment_id, customer_rating, technician_rating, review_text, review_date, helpfulness_score)
SELECT 
    sa.assignment_id,
    FLOOR(3 + (RAND() * 3)) AS customer_rating,
    FLOOR(3 + (RAND() * 3)) AS technician_rating,
    CASE 
        WHEN sa.assignment_id % 5 = 0 THEN 'Excellent service! Highly recommended.'
        WHEN sa.assignment_id % 5 = 1 THEN 'Good work. Very professional and timely.'
        -- ... more variations
    END,
    DATE_ADD(sa.actual_completion_date, INTERVAL 2 HOUR),
    FLOOR(5 + (RAND() * 15)) AS helpfulness_score
FROM Service_Assignment sa
WHERE sa.assignment_status = 'completed' 
    AND sa.actual_completion_date IS NOT NULL
LIMIT 20;

-- ============================================
-- ADDITIONAL QUERIES AND VIEWS
-- ============================================

-- View: Technician Rating Summary (Derived Attribute: rating_average)
CREATE VIEW Technician_Rating_View AS
SELECT 
    t.technician_id,
    u.first_name,
    u.last_name,
    ROUND(AVG(r.technician_rating), 2) as rating_average,
    COUNT(r.review_id) as total_reviews,
    COUNT(sa.assignment_id) as total_jobs_completed
FROM Technician t
JOIN User u ON t.user_id = u.user_id
LEFT JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
LEFT JOIN Review r ON sa.assignment_id = r.assignment_id
WHERE sa.assignment_status = 'completed'
GROUP BY t.technician_id, u.first_name, u.last_name;

-- View: Popular Service Categories
CREATE VIEW Popular_Categories_View AS
SELECT 
    sc.category_id,
    sc.category_name,
    COUNT(rr.request_id) as total_requests,
    ROUND(AVG(r.customer_rating), 2) as average_rating,
    sc.base_service_charge
FROM Service_Category sc
LEFT JOIN Repair_Request rr ON sc.category_id = rr.category_id
LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
LEFT JOIN Review r ON sa.assignment_id = r.assignment_id
GROUP BY sc.category_id, sc.category_name, sc.base_service_charge
ORDER BY total_requests DESC;

-- View: Customer Service History
CREATE VIEW Customer_Service_History AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    COUNT(rr.request_id) as total_requests,
    COUNT(CASE WHEN sa.assignment_status = 'completed' THEN 1 END) as completed_requests,
    SUM(p.payment_amount) as total_spent
FROM User u
LEFT JOIN Repair_Request rr ON u.user_id = rr.customer_id
LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
LEFT JOIN Payment p ON sa.assignment_id = p.assignment_id
WHERE u.user_type = 'customer'
GROUP BY u.user_id, u.first_name, u.last_name, u.email;

-- View: Technician Earnings Summary
CREATE VIEW Technician_Earnings_View AS
SELECT 
    t.technician_id,
    u.first_name,
    u.last_name,
    COUNT(sa.assignment_id) as total_assignments,
    COUNT(CASE WHEN sa.assignment_status = 'completed' THEN 1 END) as completed_jobs,
    SUM(CASE WHEN sa.assignment_status = 'completed' THEN sa.service_cost ELSE 0 END) as total_earnings,
    ROUND(AVG(CASE WHEN sa.assignment_status = 'completed' THEN sa.service_cost END), 2) as avg_job_cost
FROM Technician t
JOIN User u ON t.user_id = u.user_id
LEFT JOIN Service_Assignment sa ON t.technician_id = sa.technician_id
GROUP BY t.technician_id, u.first_name, u.last_name;

-- View: Pending Requests by Location
CREATE VIEW Pending_Requests_By_Location AS
SELECT 
    l.location_id,
    l.area_name,
    l.city,
    COUNT(rr.request_id) as pending_requests
FROM Location l
JOIN User u ON l.location_id = u.location_id
JOIN Repair_Request rr ON u.user_id = rr.customer_id
WHERE rr.status IN ('pending', 'assigned')
GROUP BY l.location_id, l.area_name, l.city
ORDER BY pending_requests DESC;

-- ============================================
-- SAMPLE COMPLEX QUERIES
-- ============================================

-- Query 1: Find top 5 technicians by rating
SELECT * FROM Technician_Rating_View 
ORDER BY rating_average DESC, total_reviews DESC 
LIMIT 5;

-- Query 2: Get all repair requests with customer and technician details
SELECT 
    rr.request_id,
    CONCAT(cu.first_name, ' ', cu.last_name) as customer_name,
    cu.email as customer_email,
    sc.category_name,
    rr.issue_description,
    rr.priority_level,
    rr.status,
    CONCAT(tu.first_name, ' ', tu.last_name) as technician_name,
    sa.assignment_status,
    sa.service_cost
FROM Repair_Request rr
JOIN User cu ON rr.customer_id = cu.user_id
JOIN Service_Category sc ON rr.category_id = sc.category_id
LEFT JOIN Service_Assignment sa ON rr.request_id = sa.request_id
LEFT JOIN Technician t ON sa.technician_id = t.technician_id
LEFT JOIN User tu ON t.user_id = tu.user_id
ORDER BY rr.request_date DESC;

-- Query 3: Monthly revenue summary
SELECT 
    DATE_FORMAT(p.payment_date, '%Y-%m') as month,
    COUNT(p.payment_id) as total_transactions,
    SUM(p.payment_amount) as total_revenue,
    AVG(p.payment_amount) as avg_transaction_value
FROM Payment p
WHERE p.payment_status = 'completed'
GROUP BY DATE_FORMAT(p.payment_date, '%Y-%m')
ORDER BY month DESC;

-- Query 4: Technicians with their specializations
SELECT 
    t.technician_id,
    CONCAT(u.first_name, ' ', u.last_name) as technician_name,
    GROUP_CONCAT(ts.specialization SEPARATOR ', ') as specializations,
    t.experience_years,
    t.availability_status
FROM Technician t
JOIN User u ON t.user_id = u.user_id
JOIN Technician_Specialization ts ON t.technician_id = ts.technician_id
GROUP BY t.technician_id, u.first_name, u.last_name, t.experience_years, t.availability_status;

-- Query 5: Customer satisfaction analysis
SELECT 
    sc.category_name,
    COUNT(r.review_id) as total_reviews,
    ROUND(AVG(r.customer_rating), 2) as avg_customer_rating,
    ROUND(AVG(r.technician_rating), 2) as avg_technician_rating,
    COUNT(CASE WHEN r.customer_rating >= 4 THEN 1 END) as positive_reviews,
    ROUND(COUNT(CASE WHEN r.customer_rating >= 4 THEN 1 END) * 100.0 / COUNT(r.review_id), 2) as satisfaction_percentage
FROM Review r
JOIN Service_Assignment sa ON r.assignment_id = sa.assignment_id
JOIN Repair_Request rr ON sa.request_id = rr.request_id
JOIN Service_Category sc ON rr.category_id = sc.category_id
GROUP BY sc.category_name
ORDER BY avg_customer_rating DESC;

-- Query 6: Find available technicians by specialization and location
SELECT 
    t.technician_id,
    CONCAT(u.first_name, ' ', u.last_name) as technician_name,
    u.phone_number,
    ts.specialization,
    l.area_name,
    l.city,
    t.availability_status,
    COALESCE(trv.rating_average, 0) as rating
FROM Technician t
JOIN User u ON t.user_id = u.user_id
JOIN Location l ON u.location_id = l.location_id
JOIN Technician_Specialization ts ON t.technician_id = ts.technician_id
LEFT JOIN Technician_Rating_View trv ON t.technician_id = trv.technician_id
WHERE t.availability_status = 'available'
ORDER BY rating DESC, t.experience_years DESC;

-- Query 7: Payment analysis by method
SELECT 
    payment_method,
    COUNT(*) as transaction_count,
    SUM(payment_amount) as total_amount,
    AVG(payment_amount) as avg_amount,
    MIN(payment_amount) as min_amount,
    MAX(payment_amount) as max_amount
FROM Payment
WHERE payment_status = 'completed'
GROUP BY payment_method
ORDER BY total_amount DESC;

-- Query 8: Service turnaround time analysis
SELECT 
    sc.category_name,
    AVG(DATEDIFF(sa.actual_completion_date, sa.assignment_date)) as avg_turnaround_days,
    MIN(DATEDIFF(sa.actual_completion_date, sa.assignment_date)) as min_turnaround_days,
    MAX(DATEDIFF(sa.actual_completion_date, sa.assignment_date)) as max_turnaround_days,
    COUNT(*) as completed_jobs
FROM Service_Assignment sa
JOIN Repair_Request rr ON sa.request_id = rr.request_id
JOIN Service_Category sc ON rr.category_id = sc.category_id
WHERE sa.assignment_status = 'completed' AND sa.actual_completion_date IS NOT NULL
GROUP BY sc.category_name
ORDER BY avg_turnaround_days;

-- ============================================
-- STORED PROCEDURES
-- ============================================

-- Stored Procedure 1: Assign technician to repair request
DELIMITER //
CREATE PROCEDURE AssignTechnicianToRequest(
    IN p_request_id INT,
    IN p_technician_id INT,
    IN p_service_cost DECIMAL(8,2)
)
BEGIN
    DECLARE v_assignment_date DATETIME;
    DECLARE v_estimated_date DATE;
    
    SET v_assignment_date = NOW();
    SET v_estimated_date = DATE_ADD(CURDATE(), INTERVAL 3 DAY);
    
    -- Insert assignment
    INSERT INTO Service_Assignment (
        request_id, 
        technician_id, 
        assignment_date, 
        estimated_completion_date, 
        assignment_status, 
        service_cost
    ) VALUES (
        p_request_id,
        p_technician_id,
        v_assignment_date,
        v_estimated_date,
        'assigned',
        p_service_cost
    );
    
    -- Update repair request status
    UPDATE Repair_Request 
    SET status = 'assigned' 
    WHERE request_id = p_request_id;
    
    -- Update technician availability
    UPDATE Technician 
    SET availability_status = 'busy' 
    WHERE technician_id = p_technician_id;
    
    SELECT 'Assignment created successfully' AS message;
END //
DELIMITER ;

-- Stored Procedure 2: Complete service and process payment
DELIMITER //
CREATE PROCEDURE CompleteServiceAndPayment(
    IN p_assignment_id INT,
    IN p_payment_method VARCHAR(20),
    IN p_transaction_ref VARCHAR(100)
)
BEGIN
    DECLARE v_service_cost DECIMAL(8,2);
    DECLARE v_technician_id INT;
    
    -- Get service cost and technician
    SELECT service_cost, technician_id 
    INTO v_service_cost, v_technician_id
    FROM Service_Assignment 
    WHERE assignment_id = p_assignment_id;
    
    -- Update assignment status
    UPDATE Service_Assignment 
    SET assignment_status = 'completed',
        actual_completion_date = CURDATE()
    WHERE assignment_id = p_assignment_id;
    
    -- Create payment record
    INSERT INTO Payment (
        assignment_id,
        payment_amount,
        payment_method,
        payment_date,
        payment_status,
        transaction_reference
    ) VALUES (
        p_assignment_id,
        v_service_cost,
        p_payment_method,
        NOW(),
        'completed',
        p_transaction_ref
    );
    
    -- Update technician availability
    UPDATE Technician 
    SET availability_status = 'available' 
    WHERE technician_id = v_technician_id;
    
    -- Update repair request status
    UPDATE Repair_Request rr
    JOIN Service_Assignment sa ON rr.request_id = sa.request_id
    SET rr.status = 'completed'
    WHERE sa.assignment_id = p_assignment_id;
    
    SELECT 'Service completed and payment processed' AS message;
END //
DELIMITER ;

-- Stored Procedure 3: Get technician dashboard data
DELIMITER //
CREATE PROCEDURE GetTechnicianDashboard(IN p_technician_id INT)
BEGIN
    -- Basic info
    SELECT 
        t.technician_id,
        CONCAT(u.first_name, ' ', u.last_name) as name,
        u.email,
        u.phone_number,
        t.experience_years,
        t.availability_status,
        COALESCE(trv.rating_average, 0) as rating,
        COALESCE(trv.total_reviews, 0) as total_reviews
    FROM Technician t
    JOIN User u ON t.user_id = u.user_id
    LEFT JOIN Technician_Rating_View trv ON t.technician_id = trv.technician_id
    WHERE t.technician_id = p_technician_id;
    
    -- Earnings summary
    SELECT * FROM Technician_Earnings_View 
    WHERE technician_id = p_technician_id;
    
    -- Recent assignments
    SELECT 
        sa.assignment_id,
        rr.request_id,
        CONCAT(cu.first_name, ' ', cu.last_name) as customer_name,
        sc.category_name,
        rr.issue_description,
        sa.assignment_date,
        sa.assignment_status,
        sa.service_cost
    FROM Service_Assignment sa
    JOIN Repair_Request rr ON sa.request_id = rr.request_id
    JOIN User cu ON rr.customer_id = cu.user_id
    JOIN Service_Category sc ON rr.category_id = sc.category_id
    WHERE sa.technician_id = p_technician_id
    ORDER BY sa.assignment_date DESC
    LIMIT 10;
END //
DELIMITER ;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function 1: Calculate technician rating
DELIMITER //
CREATE FUNCTION GetTechnicianRating(p_technician_id INT) 
RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    DECLARE v_rating DECIMAL(3,2);
    
    SELECT COALESCE(AVG(r.technician_rating), 0)
    INTO v_rating
    FROM Review r
    JOIN Service_Assignment sa ON r.assignment_id = sa.assignment_id
    WHERE sa.technician_id = p_technician_id;
    
    RETURN v_rating;
END //
DELIMITER ;

-- Function 2: Calculate total earnings for technician
DELIMITER //
CREATE FUNCTION GetTechnicianEarnings(p_technician_id INT, p_start_date DATE, p_end_date DATE)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_earnings DECIMAL(10,2);
    
    SELECT COALESCE(SUM(sa.service_cost), 0)
    INTO v_earnings
    FROM Service_Assignment sa
    WHERE sa.technician_id = p_technician_id
        AND sa.assignment_status = 'completed'
        AND sa.assignment_date BETWEEN p_start_date AND p_end_date;
    
    RETURN v_earnings;
END //
DELIMITER ;

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger 1: Update repair request status when assignment is created
DELIMITER //
CREATE TRIGGER after_assignment_insert
AFTER INSERT ON Service_Assignment
FOR EACH ROW
BEGIN
    UPDATE Repair_Request 
    SET status = 'assigned' 
    WHERE request_id = NEW.request_id;
END //
DELIMITER ;

-- Trigger 2: Prevent deletion of technician with active assignments
DELIMITER //
CREATE TRIGGER before_technician_delete
BEFORE DELETE ON Technician
FOR EACH ROW
BEGIN
    DECLARE v_active_count INT;
    
    SELECT COUNT(*) INTO v_active_count
    FROM Service_Assignment
    WHERE technician_id = OLD.technician_id
        AND assignment_status IN ('assigned', 'in_progress');
    
    IF v_active_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete technician with active assignments';
    END IF;
END //
DELIMITER ;

-- Trigger 3: Validate payment amount matches service cost
DELIMITER //
CREATE TRIGGER before_payment_insert
BEFORE INSERT ON Payment
FOR EACH ROW
BEGIN
    DECLARE v_service_cost DECIMAL(8,2);
    
    SELECT service_cost INTO v_service_cost
    FROM Service_Assignment
    WHERE assignment_id = NEW.assignment_id;
    
    IF NEW.payment_amount != v_service_cost THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment amount must match service cost';
    END IF;
END //
DELIMITER ;

DELIMITER ;

-- ============================================
-- SAMPLE DATA VERIFICATION QUERIES
-- ============================================

-- Count records in each table
SELECT 'Location' as TableName, COUNT(*) as RecordCount FROM Location
UNION ALL
SELECT 'User', COUNT(*) FROM User
UNION ALL
SELECT 'Technician', COUNT(*) FROM Technician
UNION ALL
SELECT 'Technician_Specialization', COUNT(*) FROM Technician_Specialization
UNION ALL
SELECT 'Service_Category', COUNT(*) FROM Service_Category
UNION ALL
SELECT 'Repair_Request', COUNT(*) FROM Repair_Request
UNION ALL
SELECT 'Service_Assignment', COUNT(*) FROM Service_Assignment
UNION ALL
SELECT 'Payment', COUNT(*) FROM Payment
UNION ALL
SELECT 'Review', COUNT(*) FROM Review;