# **HealthMaker-DRF-Project**

![ERD of HealthMaker](ERD%20(HealthMaker).png)


## **User Flow**
The application allows **guests** to register via the **UserRegistration** endpoint. During registration, users provide their details and choose a role: **client** or **coach**. Upon successful registration, the guest becomes an **authenticated user** with a defined role. Each role grants specific actions and permissions, tailored to the user’s responsibilities. **Authenticated users** can access endpoints based on their role and associated permissions.

---

## **Technical Details**
This project is designed with a **robust and scalable architecture** that enforces **role-based access control** and efficient data management.

---

## **Core Features**

### **Authentication & Authorization**
- Implemented **JWT Authentication** for secure user authentication across endpoints.
- Used **global settings** to enforce consistent authentication, permissions, and pagination throughout the project.
- Developed **custom permissions** for granular access control:
  - **ClientPermission**
  - **CoachPermission**
  - **AdminPermission**
  - **DefaultPermission**

  These permissions ensure each role has access only to its intended functionalities, reducing redundancy and improving maintainability.

---

### **Model Design**
- Adopted **user model abstraction** by extending the base user model to include additional fields like **role**.
- Applied **unique constraints** and **database indexing** to ensure data integrity and improve query performance.
- Established strong relationships between models to reflect real-world associations.
- Used **SlugField** and **UUIDField** to enhance security and avoid exposing sensitive information like IDs in API responses.

---

### **Admin Panel Enhancements**
- Added **filtering and search capabilities** to streamline data management.
- Secured sensitive fields such as **passwords** by introducing a `password2` field for confirmation and hashing all stored passwords.

---

### **Customizations in Views and Serializers**
- Introduced **nested serializers** to display related data within endpoints where appropriate.
- Concealed sensitive fields (`id`, `created_at`) and replaced them with secure alternatives (`slug`, `uuid`) in API responses.
- Integrated custom logic into serializers and views to complement the permission system and enforce business rules.

---

### **Data Validation**
- Implemented **rigorous validation mechanisms** to ensure data integrity.

**Examples:**
- A **client** cannot assign a non-existent **coach**.
- A **client** cannot edit their name to match an existing client's name.
- A **coach** cannot manipulate another coach’s clients.
- **Passwords** must meet complexity requirements.

Validation logic is applied across **models**, **serializers**, and **views** for comprehensive error prevention.

---

### **Signals**
- Leveraged **Django signals** for event-driven actions.

**Example:**  
When a client deletes their profile, the associated **user account** is automatically removed using the `@receiver` decorator.

---

### **Dynamic Querying**
- Built **ViewSets** with dynamic query filters, allowing users to search by attributes such as **meal type** or **SlugField** via query parameters in the URL.

---

### **Scalability and Maintainability**
- Consolidated **custom permissions** into a `permissions.py` file for better organization and easier updates.
- Designed the project to be **flexible**, enabling future enhancements with minimal code changes.

---

## **Conclusion**
The **HealthMaker-DRF-Project** demonstrates best practices in **Django REST Framework** development, with a strong focus on **security**, **scalability**, and **usability**. From robust **data validation** to **role-based access control**, this project ensures **logical business workflows**, **secure interactions**, and a **user-friendly experience** for both **clients** and **coaches**.

---

## **Additional Details**

### **User Management**
- **Only dealing with users (logged users)**, not guests (just viewers).
- Each guest must choose to be a **client user** or a **coach user**.
- **Admin users** cannot be a client or a coach.

---

### **Relationships**
- Each **client** must have **1 coach**.  
- Each **coach** can have **1 or more clients** or none.  
- Each **client** can have **1 workout plan** or none.  
- Each **workout plan** can have **1 or more meals**, which must be unique per plan, or none.  
- Each **client** cannot have **2 meals** with the same **type of meal**.  
- Each **coach** can create **1 or more workout plans** or none.  
- Each **coach** can create **1 or more meals** or none.  
- Each **client** can have **1 or more recommendations** or none.  
- Each **coach** can write **1 or more recommendations per client** or none.  
- Each **recommendation** must have **1 client** and **1 coach**.

---

### **Field Requirements**
- **Client**: Must have `name`, `gender`, `age`, `coach`, `weight`, `height`, and `fitness goal`.
- **Coach**: Must have `name`, `gender`, and `age`.
- **Recommendation**: Must have `title`, `details`, `client`, and `coach`.
- **Workout Plan**: Must have `type`, `details`, `duration`, `target calories to burn`, `client`, and `coach`.
- **Meal**: Must have `type`, `food items`, `total calories`, `eating time`, `client`, `coach`, and `workout plan`.

---

### **Restricted Choices**
- **Gender**: `'male'` or `'female'`.  
- **Fitness Goal**: `'Lose Weight'`, `'Build Muscles'`, or `'Special Program'`.  
- **Workout Plan**: `'GYM'`, `'Cardio'`, `'GYM & Cardio'`, or `'Special Sport'`.  
- **Meal**: `'Breakfast'`, `'Lunch'`, `'Dinner'`, or `'Snack'`.

---

### **Authentication**
- **Registration endpoint**: Open to anyone.
- **JWT token**: Required for accessing other endpoints.

---

### **Permissions**

**Client**:  
- Full control of their profile.  
- View-only access to their **coach's profile** (no add, edit, or delete).  
- View-only access to their **recommendations**, **workouts**, or **meals**.  
- Cannot add, modify, or delete their own recommendations, workouts, or meals.

**Coach**:  
- Full control of their profile.  
- View-only access to their **clients' profiles** (no add, edit, or delete).  
- Full control of their **recommendations**, **workouts**, or **meals**.

**Admin**:  
- View-only access to any endpoint (no add, edit, or delete).
- Has full ability within admin panel.
