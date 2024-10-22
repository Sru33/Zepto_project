# Rule Engine UI

## Overview
Rule Engine UI is a web application that allows users to create, combine, and evaluate rules dynamically. This tool is designed for users who need to manage complex rule sets for data validation, business logic, or decision-making processes. The application provides an intuitive interface for rule creation, combination, and evaluation, making it accessible for both technical and non-technical users.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Design Choices](#design-choices)
- [Contact](#contact)


## Features
- **Create Rules**: Users can define custom rules using a simple form.
- **Combine Rules**: Multiple rules can be combined using logical operators (AND).
- **Evaluate Rules**: Users can evaluate combined rules against a set of data.
- **Dynamic UI**: A responsive design ensures usability across various devices.

## Requirements
Before you begin, ensure you have the following installed on your machine:
- **Node.js** (version 14 or later)
- **npm** (comes with Node.js)
- **Docker** (for containerized dependencies)
- **Git** (to clone the repository)



## Installation
Follow these steps to set up and run the application locally.

### Clone the Repository
```bash
git clone https://github.com/username/rule-engine-ui.git
cd rule-engine-ui
Install Dependencies
Run the following command to install the necessary Node.js packages:

npm start
This will start the web server at http://localhost:3000.

Example Rule Creation
Navigate to the application in your web browser.
Use the "Create Rule" section to define a new rule.
Combine rules using the "Combine Rules" section.
Evaluate the combined rule against sample data in the "Evaluate Rule" section.
Rule Format
The rules should be defined in the format:
attribute operator value
For example:
age > 21
status = 'active'
Design Choices
React: The application is built using React for a dynamic and responsive user interface, allowing for a component-based architecture that enhances maintainability.
State Management: The useState hook is used for managing the application state, providing a simple and effective way to handle state changes.
CSS for Styling: The application uses a separate CSS file for styling, ensuring that the UI is clean and user-friendly.
Logical Evaluation: The evaluation logic is designed to parse and evaluate rules based on simple conditions, supporting common operators such as >, <, and =.
Docker: Docker is utilized for containerizing any potential database service, making it easy to manage dependencies and ensuring consistency across development and production environments.



Author: Srushti M P
Email: srushtimp33@gmail.com