# Django Social Media Application (Task)

## End Goals
### Overview
  A Social Platform to share post and connect with other users.

### Requirements
1. Each user can signup with name, mobile (Unique), email and password.
2. Each user can login with mobile and password
3. Each user can
    - Connect with other users
    - Add new post along with who can view it (text and images)
    - Search for other users by name, email and contact number
    - Connected users should come on top in search
4. Search Functionality
    - Search autocomplete showing predictions from connected users
    - Search Results should have “Add Connection” if user is not
      already connected
    - Search results when clicked should take to selected user profile
5. User/Connection Profile page
    - User profile should show Connected users
    - Connection profile should show all and mutual connections separately

### Specifications
1. Django
2. PostgreSQL
3. HTML, CSS
4. Javascript

## Working

The application is made with Django and Bootstrap 4 for the UI, it consists of a `Users` authentication custom model in Django which allows user to login through phone number and password.
For each page, a corresponding functional view is linked as to process the functionality of the feature.

## Screenshots

![Screenshot from 2021-09-28 12-03-28](https://user-images.githubusercontent.com/32628578/135038683-be1b1b0e-aefc-4c09-841f-57df5c0da786.png)
![Screenshot from 2021-09-28 12-21-15](https://user-images.githubusercontent.com/32628578/135038747-1a96d1fe-bcb7-4060-a241-0e74d50200ba.png)
![Screenshot from 2021-09-28 12-21-38](https://user-images.githubusercontent.com/32628578/135038763-eced8b60-fe8c-4127-833e-3764dd4ec6f1.png)
![Screenshot from 2021-09-28 12-22-35](https://user-images.githubusercontent.com/32628578/135038792-72b9c39e-cd32-4d75-89ed-51a158806812.png)
![Screenshot from 2021-09-28 12-21-58](https://user-images.githubusercontent.com/32628578/135038859-441b28e7-d8ed-431c-8668-4c375a0b690c.png)


