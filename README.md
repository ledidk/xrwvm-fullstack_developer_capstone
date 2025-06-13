# Full Stack Application Development Project V2

Welcome to my Full Stack Application Development Project V2! This project showcases my skills and knowledge in full stack development, as part of the IBM Full Stack Developer Professional Certificate. I have designed and implemented a dynamic user experience using a variety of modern technologies.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Description
In this capstone project, I designed and built a micro-services based application that leverages modern web technologies to create a dynamic and user-friendly experience. This project demonstrates my ability to handle both the front-end and back-end aspects of web development, including the use of containerization and orchestration tools for deployment.

## Features
- Dynamic user interface built with REACT
- Robust back-end services using Python and Django
- Data management with MongoDB
- Authentication and user management
- Continuous integration and deployment with GitHub Actions
- Containerized application with Docker and Kubernetes

## Technologies Used
- **Front-End**: REACT
- **Back-End**: Python, Django
- **Database**: MongoDB
- **Version Control**: Git, GitHub
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Installation

Clone the repository:
```bash
git clone https://github.com/ledidk/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone/

step 1

cd xrwvm-fullstack_developer_capstone/server
source env/Scripts/activate

step 2 

cd xrwvm-fullstack_developer_capstone/server/frontend
npm install
npm run build

step 3

cd xrwvm-fullstack_developer_capstone/server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

step 4

cd xrwvm-fullstack_developer_capstone/server
python manage.py runserver

