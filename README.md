# Expense Tracker Website

Our Expense Tracker website is a powerful tool designed to help users efficiently manage and track their expenses. Built using Django, HTML, CSS, and JavaScript, this web application provides a seamless and user-friendly experience.

## Key Features

1. **Intuitive User Interface**
   - Designed with simplicity and ease of use in mind, our website ensures that users can quickly navigate through their expense data.

2. **Data Visualization with Chart.js**
   - Leveraging the power of Chart.js, the application offers insightful visualizations of expense data. Users can easily understand their spending patterns through dynamic charts and graphs.

3. **Ajax Search Functionality**
   - The website includes an advanced search feature powered by Ajax. This allows users to search through their expenses in real-time without the need to reload the page, providing a smooth and efficient user experience.

4. **Email Verification**
   - To ensure the security and authenticity of user accounts, our application implements email verification. Users receive a verification link upon registration, enhancing the overall security of the platform.

## Technologies Used

- Django
- HTML
- CSS
- JavaScript

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Swam244/Expense_tracker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Expense_tracker
    ```

3. Create a virtual environment and activate it:
    ```bash
    pipenv shell
    ```

4. Install the required dependencies:
    ```bash
    pipenv install
    ```
7. Make Changes in environment variables in the .env file:
    ###### Create a .env file in the root folder and set your corresponding values to these variables.
    ####
    ###### 1. If using another database than default.
    ```bash
    DB_NAME = "Your Database name"
    DB_USER = "User on your Database"
    DB_PASS = "Password"
    HOST = "localhost"
    EMAIL_HOST_USER = "Your email host for sending mail"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_PASSWORD = "Host password(generated thru third party feature of google mail)"
    DEFAULT_FROM_EMAIL = ""
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    ```
    ####
    ###### 2. If using Django's default sqlite3 database.
    ```bash
    EMAIL_HOST_USER = "Your email host for sending mail"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_PASSWORD = "Host password(generated thru third party feature of google mail)"
    DEFAULT_FROM_EMAIL = ""
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    ```
    and also make changes in the database section of settings.py, it should look like this
    ![screenshot](img/screenshot.png)
    

5. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
8. Run the development server:
    ```bash
    python manage.py runserver
    ```

9. Open your web browser and go to `http://127.0.0.1:8000/` to view the website.






