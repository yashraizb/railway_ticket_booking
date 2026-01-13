# 🚂 Railway Ticket Booking System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.x-green.svg" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.x-red.svg" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/JWT-Authentication-orange.svg" alt="JWT">
  <img src="https://img.shields.io/badge/Design%20Patterns-5+-purple.svg" alt="Design Patterns">
</p>

<p align="center">
  <strong>A Railway Ticket Booking REST API demonstrating enterprise-level software architecture with multiple design patterns, clean code principles, and robust error handling.</strong>
</p>

---

## 📋 Table of Contents

| Section | Description |
|---------|-------------|
| [Overview](#-overview) | Project introduction and skills demonstrated |
| [Key Features](#-key-features) | Core functionalities |
| [Tech Stack](#-tech-stack) | Technologies used |
| [📄 Architecture & Design Patterns](docs/ARCHITECTURE.md) | Facade, Strategy, Factory, Command, Service Layer patterns |
| [📄 Project Structure](docs/PROJECT_STRUCTURE.md) | Directory layout and responsibilities |
| [📄 Database Schema](docs/DATABASE.md) | Entity relationships and models |
| [📄 API Endpoints](docs/API.md) | REST API documentation |
| [📄 Business Logic](docs/BUSINESS_LOGIC.md) | Seat booking algorithm, refunds, transactions |
| [📄 Installation & Setup](docs/SETUP.md) | How to run the project |
| [Future Enhancements](#-future-enhancements) | Roadmap |
| [Author](#-author) | Contact information |

---

## 🎯 Overview

This project is a **full-featured Railway Ticket Booking System** built as a RESTful API, simulating the core functionalities of real-world railway reservation systems like IRCTC. It demonstrates professional software development practices including:

- **Clean Architecture** with separation of concerns across multiple layers
- **Gang of Four (GoF) Design Patterns** for maintainable and extensible code
- **ACID-compliant transactions** for data integrity
- **JWT-based authentication** for secure API access
- **Comprehensive error handling** with custom exceptions

### What This Project Demonstrates

| Skill Area | Implementation |
|------------|----------------|
| **Backend Development** | Django REST Framework with class-based views |
| **Database Design** | Relational schema with foreign keys and constraints |
| **Design Patterns** | Facade, Strategy, Factory, Command, Service Layer |
| **Transaction Management** | Atomic operations with rollback support |
| **Authentication** | JWT tokens with refresh mechanism |
| **Error Handling** | Custom exceptions with HTTP status code mapping |
| **Code Organization** | Modular structure with clear separation of concerns |

### Why This Architecture?

The system is designed to handle **concurrent seat bookings** while preventing race conditions, support **partial cancellations** with proportional refunds, and maintain **data consistency** even when operations fail mid-process.

---

## ✨ Key Features

### 🎫 Booking Management
- **Search Trains** - Find trains between stations with available seat counts
- **Book Multiple Seats** - Book seats for multiple passengers in a single transaction
- **Smart Seat Allocation** - Algorithm considers segment-based availability
- **PNR Generation** - Unique booking reference for each reservation

### 🔄 Cancellation & Refund
- **Full Cancellation** - Cancel entire booking with automatic refund calculation
- **Partial Cancellation** - Cancel specific passengers while keeping others
- **Dynamic Refund Policy**:
  | Days Before Journey | Refund |
  |---------------------|--------|
  | > 7 days | 100% |
  | 3-7 days | 50% |
  | 1-3 days | 25% |
  | < 1 day | 0% |

### 🔐 Security & Data Integrity
- **JWT Authentication** with token refresh
- **Atomic Transactions** with rollback support
- **Race Condition Prevention** using `SELECT FOR UPDATE`
- **Failure Tracking** - Persist failed states for debugging

➡️ **[Read more in Business Logic documentation](docs/BUSINESS_LOGIC.md)**

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **Django 4.x** | Web framework with ORM |
| **Django REST Framework** | RESTful API development |
| **Simple JWT** | JWT token authentication |
| **SQLite** / **PostgreSQL** | Database |

➡️ **[Installation instructions](docs/SETUP.md)**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [🏗️ Architecture & Design Patterns](docs/ARCHITECTURE.md) | Detailed explanation of Facade, Strategy, Factory, Command, and Service Layer patterns with code examples |
| [📁 Project Structure](docs/PROJECT_STRUCTURE.md) | Complete directory layout with layer architecture diagram |
| [🗄️ Database Schema](docs/DATABASE.md) | Entity relationships, model descriptions, status enums |
| [🔌 API Endpoints](docs/API.md) | Full API documentation with request/response examples |
| [💡 Business Logic](docs/BUSINESS_LOGIC.md) | Seat booking algorithm, refund calculation, transaction management |
| [🚀 Installation & Setup](docs/SETUP.md) | Quick start guide, environment config, troubleshooting |

---

## 🔮 Future Enhancements

- [ ] **Payment Gateway Integration** - Razorpay/Stripe
- [ ] **Email Notifications** - Booking confirmations, cancellation alerts
- [ ] **Waiting List Management** - Automatic ticket confirmation
- [ ] **Admin Dashboard** - Analytics and reports
- [ ] **Rate Limiting** - API throttling
- [ ] **Caching** - Redis for frequently accessed data
- [ ] **Docker Support** - Containerized deployment
- [ ] **CI/CD Pipeline** - Automated testing and deployment

---

## 👤 Author

**Yash Rai**

- GitHub: [@yourusername](https://github.com/yashraizb)
- LinkedIn: [Yash Rai](www.linkedin.com/in/yashrai0202)
- Email: yashraizb@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong>
</p>
