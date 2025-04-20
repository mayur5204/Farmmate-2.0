# Farmmate Project

A comprehensive agriculture management web application that helps farmers make informed decisions through crop recommendations, weather forecasting, and resource management.

## Features

- **Crop Recommendation System**: Analyzes soil parameters and environmental conditions to recommend suitable crops
- **Weather Forecast**: Provides weather information to help with farming decisions
- **User Authentication**: Secure login and registration system
- **Resource Center**: Information on farming practices and resources
- **Products Showcase**: Display of farming products and solutions

## Project Structure

The project is organized into specialized Django apps:

- **home**: Core pages and navigation
- **crop_recommendation**: Crop recommendation system using machine learning
- **users**: User authentication and management
- **weather**: Weather forecasting functionality

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Technology Stack

- Django web framework
- SQLite database
- Machine learning for crop recommendation
- Bootstrap for responsive design