# AMK Task Manager

A Django-based Task Management Application with role-based access, JWT authentication, and a custom admin panel. This project was completed as a company assignment with a 1-day deadline.

---

## Project Requirements & How They Are Satisfied

### 1. Task Completion Report & Worked Hours
- When users mark a task as completed, they must submit a Completion Report and Worked Hours.
- These reports are visible to Admins and SuperAdmins for review and monitoring.
- **Implemented:**
  - Task model includes `completion_report` and `worked_hours` fields.
  - API and admin panel enforce report and hours on completion.

### 2. API Endpoints
- **JWT Authentication:**
  - `/api/token/` (POST): Authenticate with username/password, receive JWT token.
  - `/api/token/refresh/` (POST): Refresh JWT token.
- **Tasks APIs:**
  - `/tasks` (GET): Fetch all tasks assigned to the logged-in user.
  - `/tasks/{id}` (PUT): Update status, submit report & hours when marking as completed.
  - `/tasks/{id}/report` (GET): Admins/SuperAdmins can view report & hours for completed tasks.
- **Implemented:** All endpoints above are present and validated.

### 3. Admin Panel (Custom HTML Templates)
- **SuperAdmin Features:**
  - View/manage all users (create, delete, assign roles)
  - View/manage all admins (create, delete, assign roles, promote/demote)
  - Assign users to admins
  - View/manage all tasks across users
  - View task reports
- **Admin Features:**
  - Assign tasks to users
  - View/manage tasks assigned to their users
  - View completion reports (including worked hours)
  - Cannot manage user roles
- **Implemented:** All features above are present in the custom admin panel (`/admin/users/`, `/admin/admins/`, `/admin/tasks/`, etc.)

### 4. Task Workflow & Roles
- **Roles:** SuperAdmin, Admin, User (using Django Groups)
- **Permissions:**
  - SuperAdmin: Full access
  - Admin: Task management for managed users
  - User: Can only interact with own tasks
- **Implemented:** Role-based access enforced in views and templates.

### 5. Task Model
- Fields: Title, Description, Assigned To, Due Date, Status, Completion Report, Worked Hours
- **Implemented:** All fields present in `tasks/models.py`.

### 6. Completion Report & Worked Hours
- Required when marking a task as completed (API and admin panel)
- **Implemented:** Validation in forms and serializers.

### 7. Database & Requirements
- Uses SQLite
- `requirements.txt` includes all necessary packages

---

## Step-by-Step Setup

### 1. Prerequisites
- Python 3.12+
- Docker & Docker Compose
- (Optional) VS Code for debugging

### 2. Clone the Project
```bash
git clone <your-repo-url>
cd AMK_Task_Manager
```

### 3. Install Docker & Docker Compose (Linux)
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

### 4. Build and Run the App
```bash
docker-compose up --build
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the app.

### 5. Create a SuperAdmin User
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 6. Fix UserProfile for SuperAdmin (if needed)
If you get a `User has no userprofile` error, run:
```bash
python manage.py shell
```
Then in the shell:
```python
from django.contrib.auth.models import User
from tasks.models import UserProfile
user = User.objects.get(username='your_superuser_username')
UserProfile.objects.get_or_create(user=user)
exit()
```

### 7. Log In
- Go to [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
- Use your superuser credentials

### 8. Admin Panel Usage
- **Custom Admin Panel:** `/admin/users/`, `/admin/admins/`, `/admin/tasks/` etc.
- **Django Admin Site:** `/admin/` (for model management)
- **User Profile:** `/accounts/profile/`

### 9. API Endpoints
- Obtain JWT token: `POST /api/token/` (username, password)
- Refresh token: `POST /api/token/refresh/`
- List tasks: `GET /tasks` (JWT required)
- Update task: `PUT /tasks/{id}` (JWT required)
- View report: `GET /tasks/{id}/report` (Admin/SuperAdmin only)

---

## Roles & Permissions
- **SuperAdmin:** Manage users/admins, assign users, view all tasks/reports
- **Admin:** Assign tasks, view/manage tasks/reports for managed users
- **User:** View/update own tasks, submit completion report & worked hours

---

## Project Structure
- `core/` - Django project settings, URLs
- `tasks/` - App with models, views, serializers, forms, signals
- `templates/` - Custom HTML templates for all pages
- `requirements.txt` - Python dependencies
- `Dockerfile` & `docker-compose.yml` - Container setup

---

## UI & Customization
- Bootstrap 5 for modern look
- Theme switcher in navbar
- Responsive and mobile-friendly

---

## Troubleshooting
- **UserProfile error:** See step 6 above
- **404 on /admin/users/:** Make sure custom admin URLs are before Django admin in `urls.py`
- **Missing templates:** All required templates are provided; add more as needed

---

## Contact
For any issues, contact Noviindus Technologies.
