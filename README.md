# Django_Web_Tracking_Task
## Overview
Django Tracking Task is a web application designed to help users efficiently manage and track their daily tasks. This project leverages the robust features of Django and several other technologies to offer a seamless task management experience.

## Features
- **User Authentication**: Secure login and registration system to manage user access.
- **Task Management**: Users can add, edit, and delete tasks.
- **Task Tracking**: Monitor the completion status of tasks over a customizable date range.
- **Interactive Graphs**: Visual representation of task completion using interactive charts.
- **Mobile Friendly**: Responsive design that works well on both desktops and mobile devices.
- **Admin Dashboard**: An admin panel for managing users and tasks effectively.

## Technologies Used
- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **Plotly**: Utilized for creating interactive graphs to track task completion.
- **Bootstrap**: For responsive design that adapts to different device screens.
- **Heroku**: Cloud platform for deploying and running the application.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX, serving Django applications on Heroku.
- **PostgreSQL**: The primary database used by Heroku for storing data.
- **Git**: For version control and source code management.

## Functions Utilized
- **`generate_plot()`**: Generates interactive plots that provide a graphical view of task completion percentages over time.
- **`calculate_completion_percentage()`**: Calculates the percentage of completed tasks based on the data logged.
- **CRUD Operations**: Complete implementation of Create, Read, Update, and Delete operations for task management through Django's ORM.
- **Responsive Templates**: Leveraging Bootstrap to create templates that work on mobile and desktop browsers.

