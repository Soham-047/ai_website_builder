🧠 AI Website Builder (Django + JWT + Gemini AI)

Overview:

    Automatically create structured content for business use cases. The app supports role-based access, user management, and CRUD operations for generated websites.
  <img width="1710" alt="Screenshot 2025-05-02 at 12 21 46 AM" src="https://github.com/user-attachments/assets/4c3ad4b9-ea6e-4897-a7a7-1f5b761624b4" />


🔧 Features:

    JWT-Based Authentication: Secure login/logout flow using SimpleJWT.

    Role-Based Access Control: Supports Admin, Editor, and Viewer roles.

    AI-Powered Website Generation: Utilizes Google Gemini to generate content like hero sections, services, about pages, contact info, etc.

    User Management (Admin): Admins can manage users and roles.

    Website Management:

    Create websites using AI or manual entry.

    Edit or delete existing websites.

    Preview full content before deployment.

    Frontend with Bootstrap: Clean, responsive UI using Bootstrap 5.

    Logout Token Blacklisting: Ensures secure sign-out with JWT refresh token blacklisting.

    Custom Django User Model: Uses email-based login instead of username.

🧠 Tech Stack:

    Backend: Django, Django REST Framework, SimpleJWT

    Frontend: Django Templates, Bootstrap 5

    Database: MongoDB (via Djongo)

    AI Integration: Google Gemini API

    Environment Management: python-dotenv

📁 Modules:

    accounts: Handles authentication, registration, and user/role management.

    website: Manages website creation, listing, and editing.

    ai_generator: Integrates Gemini AI to produce website content dynamically.

📌 How It Works:

    User signs up or logs in.

    User chooses to create a website via form.

    AI generates website content, returned as JSON.

    Website is stored under the user’s account.

    User can edit, delete, or preview the site.

    
🛠️ Project Setup & Commands
✅ 1. Clone the Repository

    git clone <repo-url>
    cd <project-directory>
    
📦 2. Create and Activate Virtual Environment
    
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    
📥 3. Install Dependencies
    
    pip install -r requirements.txt
    
🔐 4. Set Up Environment Variables
    Create a .env file in the root directory:

    SECRET_KEY=your-django-secret-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    GOOGLE_API_KEY=your-google-gemini-api-key
    
🧬 5. Apply Migrations

    python manage.py makemigrations
    python manage.py migrate
    
👤 6. Create Superuser

    python manage.py createsuperuser
    
🚀 7. Run the Server

    python manage.py runserver
Then open your browser:

    http://127.0.0.1:8000/

🥳 Happy Website Building!! 🥳
