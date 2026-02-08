# QA Engineer Guide: From Zero to API Hero

Welcome! This guide is designed to help you master API testing using this project. We'll start with the basics and gradually move to more complex scenarios. This is a safe environment to experiment, so don't be afraid to break things!

### 1. What is REST?

**REST** (Representational State Transfer) is an architectural style for providing standards between computer systems on the web, making it easier for systems to communicate with each other.

Our system obeys **REST rules**, which means:
- **Resources**: Everything (Authors, Posts) is a resource identified by a URL.
- **HTTP Methods**: Use `GET` to read, `POST` to create, `PUT`/`PATCH` to update, and `DELETE` to remove.
- **Stateless**: Each request from a client contains all the information needed to understand and process the request.

---

### 2. First Steps: Reading Data

Let's try to get a list of all authors and then details about a specific one.

<details>
<summary><b>How to make requests (Swagger, Postman, curl)</b></summary>

| Tool | Steps |
| :--- | :--- |
| **Swagger** | Open `/api/docs/swagger/`, find the endpoint, click **Try it out**, then **Execute**. For protected endpoints, click the **Authorize** button at the top and enter your token as `Bearer <your_token>`. |
| **Postman** | Create a new request, select method (e.g., `GET`), enter URL (e.g., `http://127.0.0.1:8000/api/authors/`), click **Send**. |
| **curl** | Run `curl -X GET http://127.0.0.1:8000/api/authors/` in your terminal. |

</details>

**Exercise:**
1. Get the list of all authors.
2. Pick one `id` from the list and get that author's details (using `/api/authors/{id}/`).
3. Do the same for posts (`/api/posts/`).

---

### 3. Pagination: Navigating Large Data Sets

In real systems, you might have thousands of records. Sending them all at once would be slow. **Pagination** solves this by splitting data into "pages".

In many systems, you might see `offset` and `limit`. Our system uses **Page Number Pagination**.
- `page`: The page number you want to see.

**Query Parameters** are additions to the URL starting with `?`. For example: `/api/posts/?page=2`.

**Exercise:** Try to find the second and third pages of the posts list.

<details>
<summary><b>Check the answer</b></summary>

**URL:** `http://127.0.0.1:8000/api/posts/?page=2` and `http://127.0.0.1:8000/api/posts/?page=3`

- **Swagger**: Enter `2` in the `page` field under Parameters.
- **Postman**: In the **Params** tab, add Key: `page`, Value: `2`.
- **curl**: `curl -X GET "http://127.0.0.1:8000/api/posts/?page=2"`

</details>

---

### 4. Sorting and Filtering

Backends usually allow you to narrow down results.
- **Filtering**: Finding specific records (e.g., "only published posts").
- **Sorting**: Ordering records (e.g., "newest first").

In our API:
- Filter posts by status: `?status=draft` or `?status=published` or `?status=archived`.
- Sort posts: `?ordering=created_at` (ascending) or `?ordering=-created_at` (descending).

**Exercise:** Find all posts that are in **draft** status. Then, find all **archived** posts, sorted by **created_at** from newest to oldest (descending).

<details>
<summary><b>Check the answer</b></summary>

- **Drafts:** `http://127.0.0.1:8000/api/posts/?status=draft`
- **Archived Descending:** `http://127.0.0.1:8000/api/posts/?status=archived&ordering=-created_at`

</details>

---

### 5. Authentication: Who are you?

Most APIs require you to identify yourself. Popular methods include:
- **Basic Auth**: Sending username and password with every request (less secure).
- **API Keys**: A long secret string.
- **JWT (JSON Web Token)**: Our system uses this.

**Note:** Only authenticated authors can create posts. The author of the post is automatically determined by your authentication token.

**How JWT works:**
1. You **Login** with your credentials.
2. The server sends back an `access` token.
3. You include this token in the **Header** of every future request: `Authorization: Bearer <your_token>`.

**Exercise: Become an Author**
1. **Register:** Create yourself as an author.
   - `POST /api/authors/`
   - Body: `{"username": "tester", "password": "password123", "full_name": "QA Student"}`
2. **Login:** Get your token.
   - `POST /api/login/`
   - Body: `{"username": "tester", "password": "password123"}`
   - *Copy the `access` token.*
   - *In Swagger, click **Authorize** at the top and enter `Bearer <your_access_token>`.*
3. **Publish a Post:**
   - `POST /api/posts/`
   - Header: `Authorization: Bearer <your_token>`
   - Body: `{"title": "My First Post", "content": "Hello World", "status": "published"}`
4. **Edit your Post:** Change the title of your post using `PATCH /api/posts/{id}/`.

---

### 6. Final Challenge: Advanced Filtering

Now that you've created a post, try to find it in the main list using filters.

**Exercise:** Request the posts list, but filter it so it only shows posts by **your** author ID.

<details>
<summary><b>Check the answer</b></summary>

**URL:** `http://127.0.0.1:8000/api/posts/?author={your_author_id}`

Replace `{your_author_id}` with the ID you received when you registered or found in the authors list.

</details>

---

### 7. The End

Congratulations! You've covered the essentials of API testing. You can now:
- Navigate RESTful resources.
- Use Pagination, Filtering, and Sorting.
- Handle JWT Authentication.
- Perform CRUD operations.

Keep practicing and exploring the Swagger documentation for more details!
