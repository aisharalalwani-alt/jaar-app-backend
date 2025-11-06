 # 🏙️ JAAR App — Backend
![alt text](<Logo 4.png>)
## 📘 Project & Repository Description

This repository contains the backend of the **JAAR App**, a community-based platform that connects neighbors through posts, local events, and volunteer activities.
Users can create profiles, share updates, join or host events, and interact within their neighborhood.

---

## ⚙️ Tech Stack

* **Python 3**
* **Django REST Framework (DRF)**
* **PostgreSQL (or SQLite for development)**
* **JWT Authentication**

---

## 🔗 Related Links

* **Frontend Repository:** [JAAR App Frontend](https://github.com/aisharalalwani-alt/jaar-app-frontend)
* **Deployed Site:** *(Add link once deployed)*

---

## 🗂️ ERD Diagram

 ![alt text](Flowchart-1.jpg)
---

## 🚦 Routing Table

| Endpoint                 | Method     | Description                                         | Auth Required |
| ------------------------ | ---------- | --------------------------------------------------- | ------------- |
| `/api/my-profile/`       | GET        | Retrieve current user profile with posts and events | ✅             |
| `/api/my-profile/`       | PUT        | Update user profile info                            | ✅             |
| `/api/events/`           | GET / POST | List or create events                               | ✅             |
| `/api/events/<id>/`      | GET        | Retrieve specific event                             | ✅             |
| `/api/events/<id>/join/` | POST       | Join an event as volunteer                          | ✅             |
| `/api/posts/`            | GET / POST | List or create neighborhood posts                   | ✅             |
| `/api/volunteers/`       | GET        | View volunteer list                                 | ✅             |

---

## 💡 Code Highlight — Feature I’m Proud Of ✨

### `views.py`

```python
# ------------------ MY NEIGHBOR PROFILE ------------------
class MyNeighborProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the current user's profile along with their posts,
        created events, and events they've joined.
        """
        neighbor = get_object_or_404(NeighborProfile, user=request.user)
        profile_data = NeighborProfileSerializer(neighbor).data

        required_fields = ["phone", "street_name", "postal_code", "city"]
        profile_complete = all(profile_data.get(field) for field in required_fields)

        posts = Post.objects.filter(created_by=neighbor)
        posts_data = PostSerializer(posts, many=True).data

        created_events = Event.objects.filter(created_by=neighbor)
        created_events_data = EventSerializer(created_events, many=True).data

        volunteer_entries = Volunteer.objects.filter(
            name=neighbor.user.username
        ) | Volunteer.objects.filter(phone=neighbor.phone)

        joined_events = Event.objects.filter(volunteers__in=volunteer_entries).distinct()
        joined_events_data = EventSerializer(joined_events, many=True).data

        return Response({
            "profile": profile_data,
            "profile_complete": profile_complete,
            "posts": posts_data,
            "created_events": created_events_data,
            "joined_events": joined_events_data
        })
```


---

## ⚙️ Installation Instructions (Local Server)

```bash
# 1️⃣ Clone the repository
git clone https://github.com/aisharalalwani-alt/jaar-app-backend.git
cd jaar-app-backend

# 2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Mac / Linux
venv\Scripts\activate          # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5️⃣ Create a superuser
python manage.py createsuperuser

# 6️⃣ Run the development server
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000)


## ❄️ IceBox Features (Future Enhancements)

* Real-time chat between neighbors
* Event reminders via email or SMS
* Profile picture uploads
* Map integration for nearby events
* Notifications and activity feed

---

© 2025 JAAR App — Backend API
