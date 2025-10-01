# AMK Task Manager

A Django-based Task Management Application with role-based access, JWT authentication, and a custom admin panel. This project supports SuperAdmin, Admin, and User roles, and provides both a modern web UI and a REST API.

---

## Features

- Role-based access: SuperAdmin, Admin, User (using Django Groups)
- Assign/unassign users to admins (with UI)
- Task assignment, completion reports, and worked hours
- JWT authentication for API access
- Custom admin panel for user, admin, and task management
- Dockerized for easy setup

---

## Quick Start

### 1. Prerequisites
- Python 3.12+
- Docker & Docker Compose

### 2. Clone the Project
```bash
git clone <your-repo-url>
cd Task-Manager
```

### 3. Build and Run the App
You can use the provided automation scripts:

#### On Windows:
```bat
initiate.bat -b   REM Build and start containers
initiate.bat      REM Start containers (no build)
initiate.bat -d   REM Stop and remove containers
initiate.bat -r   REM Restart containers
```

#### On Linux/Mac:
```bash
./initiate.sh -b   # Build and start containers
./initiate.sh      # Start containers (no build)
./initiate.sh -d   # Stop and remove containers
./initiate.sh -r   # Restart containers
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the app.

---

## Initial Setup: Roles & Superuser

### 1. Create Default Groups (Roles)
Run this Django management command to create the User, Admin, and SuperAdmin groups:
```bash
python manage.py create_groups
```

### 2. Create a SuperAdmin User
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

**Important:** After creating a superuser, make sure they are added to the SuperAdmin group. You can do this via the Django admin site (`/admin/`) or with a shell command:
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='your_superuser_username')
group = Group.objects.get(name='SuperAdmin')
user.groups.add(group)
exit()
```

### 3. (Optional) Create Admins and Users
You can create Admins and Users via the custom admin panel or Django admin. To add them to the correct group:
```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='username')
group = Group.objects.get(name='Admin')  # or 'User'
user.groups.add(group)
```

---

## Assigning and Unassigning Users to Admins

1. Log in as SuperAdmin.
2. Go to **Admin Panel → Assign Users to Admins** (`/admin/users/assign/`).
3. Use the form to assign a user to an admin.
4. To unassign, click the **Unassign** button next to the admin in the assignments table.

---


## API Testing with Postman

Below are step-by-step instructions for testing all major features using Postman.

### 1. Obtain JWT Token

**Endpoint:** `POST /api/token/`
**Body (JSON):**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
**Response:**
```
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### 2. Refresh JWT Token

**Endpoint:** `POST /api/token/refresh/`
**Body (JSON):**
```json
{
  "refresh": "<refresh_token>"
}
```
**Response:**
```
{
  "access": "<new_access_token>"
}
```

---

### 3. List Tasks (User/Admin/SuperAdmin)

**Endpoint:** `GET /tasks`
**Headers:**
- `Authorization: Bearer <access_token>`

**Response:**
```
[
  {
    "id": 1,
    "title": "Task Title",
    "description": "...",
    "assigned_to": 2,
    "due_date": "2025-10-01",
    "status": "Pending",
    "completion_report": null,
    "worked_hours": null
  },
  ...
]
```

---

### 4. Update a Task (Mark as Completed, Add Report & Hours)

**Endpoint:** `PUT /tasks/{id}`
**Headers:**
- `Authorization: Bearer <access_token>`

**Body (JSON):**
```json
{
  "status": "Completed",
  "completion_report": "Work done details...",
  "worked_hours": 5
}
```
**Response:**
```
{
  "id": 1,
  "title": "Task Title",
  ...
  "status": "Completed",
  "completion_report": "Work done details...",
  "worked_hours": 5
}
```

---

### 5. View Task Report (Admin/SuperAdmin)

**Endpoint:** `GET /tasks/{id}/report`
**Headers:**
- `Authorization: Bearer <access_token>`

**Response:**
```
{
  "id": 1,
  "completion_report": "Work done details...",
  "worked_hours": 5
}
```

---

### 6. Assign/Unassign Users to Admins (SuperAdmin Only)

**Assign User to Admin:**
- Use the web UI at `/admin/users/assign/` (not available via API by default).

**Unassign User from Admin:**
- Use the web UI at `/admin/users/assign/` and click the "Unassign" button.

---

### 7. Create Users, Admins, and SuperAdmins

- Use Django admin (`/admin/`) or the custom admin panel (`/admin/users/`, `/admin/admins/`).
- To create via API, you’d need to expose user creation endpoints (not present by default for security).

---

### 8. Role-Based Access Testing

- **SuperAdmin:** Can access all endpoints, assign/unassign users, manage admins and users.
- **Admin:** Can assign tasks to users, view/manage only their users’ tasks.
- **User:** Can only view and update their own tasks.

Test by logging in as different roles and trying the endpoints above. You should receive `403 Forbidden` if you try to access unauthorized resources.

---

## Example Postman Workflow

1. **Login:**  
   - POST `/api/token/` with username/password.  
   - Save the `access` token.

2. **Set Authorization:**  
   - In Postman, set `Authorization` type to `Bearer Token` and paste your `access` token.

3. **List Tasks:**  
   - GET `/tasks` to see your tasks.

4. **Update Task:**  
   - PUT `/tasks/{id}` with completion data.

5. **View Report:**  
   - GET `/tasks/{id}/report` (if you are Admin/SuperAdmin).

6. **Test Permissions:**  
   - Try accessing `/tasks/{id}/report` as a User (should get 403).  
   - Try assigning users as Admin (should not be allowed).

---

## Roles & Permissions
- **SuperAdmin:** Manage users/admins, assign/unassign users, view all tasks/reports
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
- **UserProfile error:** If you get a `User has no userprofile` error, run:
    ```python
    from django.contrib.auth.models import User
    from tasks.models import UserProfile
    user = User.objects.get(username='your_superuser_username')
    UserProfile.objects.get_or_create(user=user)
    ```
- **404 on /admin/users/:** Make sure custom admin URLs are before Django admin in `urls.py`
- **Missing templates:** All required templates are provided; add more as needed

---

## Contact
For any issues, contact Abdul Muhsin
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
For any issues, contact Abdul Muhsin
