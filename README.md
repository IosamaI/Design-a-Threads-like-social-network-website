# Design-a-Threads-like-social-network-website


![network](https://github.com/user-attachments/assets/233aad74-8f06-4dad-99f2-ef9d88d37b68)


This project is a Django-based social networking platform where users can create posts, follow other users, and interact with posts by liking or editing them. The platform includes features like profile pages, pagination, and a dynamic user interface using JavaScript, HTML, and CSS.

## Features

### 1. New Post
- Users who are signed in can create new posts by entering text in a textarea and submitting it.
- Posts can be created directly from the "All Posts" page or on a dedicated "New Post" page (optional).

### 2. All Posts
- The "All Posts" page displays all posts from all users in reverse chronological order (most recent first).
- Each post displays the username of the poster, the content of the post, the date and time of posting, and the number of likes.

### 3. Profile Page
- Clicking on a username navigates to that user's profile page.
- The profile page displays:
  - Number of followers.
  - Number of users the person is following.
  - All posts made by the user in reverse chronological order.
- Users can follow or unfollow others directly from their profile page. Users cannot follow themselves.

### 4. Following Page
- The "Following" page displays posts from users that the signed-in user is following.
- Posts on this page are also displayed in reverse chronological order.
- This page is only accessible to signed-in users.

### 5. Pagination
- Pages displaying posts (e.g., All Posts, Profile, Following) only show 10 posts per page.
- A "Next" button navigates to the next set of posts, while a "Previous" button navigates back to the earlier set of posts.

### 6. Edit Post
- Users can edit their own posts by clicking an "Edit" button.
- Clicking "Edit" replaces the post content with a textarea, allowing the user to modify the text.
- The edited post can be saved without reloading the page, using JavaScript.
- For security, users cannot edit posts created by other users.

### 7. Like and Unlike
- Users can like or unlike posts by clicking a button.
- The like count updates asynchronously using JavaScript, without reloading the page.

## Technical Details

### Models
The Django `models.py` file includes the following models:
- **User**: Represents users of the platform. Inherits from Django's `AbstractUser`.
- **Post**: Represents a single post with fields for:
  - `author`: The user who created the post.
  - `content`: The text content of the post.
  - `timestamp`: The date and time the post was created.
  - `likes`: Many-to-many relationship with the User model for liking posts.
- **Follow**: Represents the follower-following relationship between users.

### Views
- **Index**: Displays the "All Posts" page.
- **Profile**: Displays a user's profile page.
- **Following**: Displays posts from followed users.
- **Post Management**: Handles creating, editing, liking, and unliking posts.

### API Endpoints
- `GET /posts`: Retrieve posts for a specific page.
- `POST /posts`: Create a new post.
- `PUT /posts/<id>`: Update a post (e.g., editing content, liking/unliking).
- `GET /profile/<username>`: Retrieve a user's profile information.
- `PUT /follow/<username>`: Follow or unfollow a user.

### Frontend
- JavaScript is used to handle dynamic interactions, such as editing posts, liking posts, and pagination.
- HTML templates are designed with Django's templating engine.
- CSS styles provide a responsive and visually appealing interface.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd project4/network
   ```

2. **Install Dependencies**
   Ensure you have Python and Django installed. Install required packages using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## File Descriptions

- **network/urls.py**: URL configurations for the app.
- **network/views.py**: Contains view functions for handling requests and responses.
- **network/models.py**: Defines the data models for the app.
- **network/templates/network**: Contains HTML templates for the app.
- **network/static/network**: Includes static files like CSS and JavaScript.

## Distinctiveness and Complexity
This project is distinct and complex due to the following features:
- Combination of backend (Django) and frontend (JavaScript) for a seamless user experience.
- Implementation of asynchronous operations (e.g., liking posts, editing posts) using JavaScript and the Fetch API.
- Dynamic pagination for scalability and performance.
- Security considerations, such as restricting post edits to the original author.
- Relational database design to manage users, posts, likes, and follows.

## Additional Requirements
Ensure the following Python packages are installed:
- Django

To install these requirements, run:
```bash
pip install Django
```

## Future Improvements
- Add support for uploading images in posts.
- Implement real-time updates using WebSockets.
- Enhance the UI with additional CSS frameworks like Bootstrap or Tailwind CSS.

---

Feel free to reach out if you have questions or need assistance with this project!
