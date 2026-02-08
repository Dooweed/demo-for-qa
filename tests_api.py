import pytest
from rest_framework import status
from authors.models import Author
from posts.models import Post, PostStatus

@pytest.fixture
def author_data():
    return {
        "username": "testauthor",
        "password": "password123",
        "full_name": "Test Author",
        "description": "Test Description"
    }

@pytest.fixture
def create_author(db, author_data):
    author = Author.objects.create(
        username=author_data["username"],
        full_name=author_data["full_name"],
        description=author_data["description"]
    )
    author.set_password(author_data["password"])
    author.save()
    return author

@pytest.fixture
def auth_client(client, create_author, author_data):
    response = client.post("/api/login/", {
        "username": author_data["username"],
        "password": author_data["password"]
    })
    token = response.data["access"]
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client

@pytest.mark.django_db
def test_public_endpoints(client, create_author):
    # Test Author list
    response = client.get("/api/authors/")
    assert response.status_code == status.HTTP_200_OK
    
    # Test Author detail
    response = client.get(f"/api/authors/{create_author.id}/")
    assert response.status_code == status.HTTP_200_OK

    # Test Post list
    response = client.get("/api/posts/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_author_authentication_and_permissions(client, auth_client, create_author, author_data):
    # Create another author
    other_author = Author.objects.create(username="other", full_name="Other Author")
    other_author.set_password("password")
    other_author.save()

    # Authenticated author tries to update themselves
    response = auth_client.patch(f"/api/authors/{create_author.id}/", {"full_name": "Updated Name"}, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["full_name"] == "Updated Name"

    # Authenticated author tries to update another author
    response = auth_client.patch(f"/api/authors/{other_author.id}/", {"full_name": "Hacker"}, content_type="application/json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Unauthenticated user tries to update author
    client.defaults.pop("HTTP_AUTHORIZATION", None)
    response = client.patch(f"/api/authors/{create_author.id}/", {"full_name": "Hacker"}, content_type="application/json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_post_creation_and_permissions(auth_client, create_author, db):
    # Create post
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "status": PostStatus.PUBLISHED
    }
    response = auth_client.post("/api/posts/", post_data, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    post_id = response.data["id"]

    # Update own post
    response = auth_client.patch(f"/api/posts/{post_id}/", {"title": "Updated Post"}, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    # Create another author and their client
    other_author = Author.objects.create(username="other2", full_name="Other Author 2")
    other_author.set_password("password")
    other_author.save()
    
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(other_author)
    import copy
    other_client = copy.deepcopy(auth_client)
    other_client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {refresh.access_token}"

    # Other author tries to update first author's post
    response = other_client.patch(f"/api/posts/{post_id}/", {"title": "Hacked Post"}, content_type="application/json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_unauthenticated_post_creation(client):
    post_data = {
        "title": "Unauthenticated Post",
        "content": "Content",
        "status": PostStatus.PUBLISHED
    }
    response = client.post("/api/posts/", post_data, content_type="application/json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_post_creation_author_inference(auth_client, create_author):
    post_data = {
        "title": "Inferred Author Post",
        "content": "Content",
        "status": PostStatus.PUBLISHED
    }
    response = auth_client.post("/api/posts/", post_data, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["author"] == create_author.id
    assert response.data["author_name"] == create_author.full_name

@pytest.mark.django_db
def test_filtering_and_sorting(auth_client, create_author):
    # Create multiple posts
    Post.objects.create(title="Post A", content="C1", author=create_author, status=PostStatus.DRAFT)
    Post.objects.create(title="Post B", content="C2", author=create_author, status=PostStatus.PUBLISHED)
    
    # Filter by status
    response = auth_client.get(f"/api/posts/?status={PostStatus.DRAFT}")
    results = response.data["results"] if isinstance(response.data, dict) else response.data
    assert len(results) == 1
    assert results[0]["title"] == "Post A"

    # Filter by author
    response = auth_client.get(f"/api/posts/?author={create_author.id}")
    results = response.data["results"] if isinstance(response.data, dict) else response.data
    assert len(results) == 2

    # Sorting
    response = auth_client.get("/api/posts/?ordering=created_at")
    results = response.data["results"] if isinstance(response.data, dict) else response.data
    assert results[0]["title"] == "Post A"
    
    response = auth_client.get("/api/posts/?ordering=-created_at")
    results = response.data["results"] if isinstance(response.data, dict) else response.data
    assert results[0]["title"] == "Post B"
