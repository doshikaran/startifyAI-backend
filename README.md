# 🚀 **StartifyAI – Backend README**  

**Empower your startup journey with AI-driven insights, health checks, and auto-generated pitch decks. This backend service handles data processing, API endpoints, and LLM integrations.**

---

## 📚 **Table of Contents**  

1. [Introduction](#introduction)  
2. [Features](#features)  
3. [System Overview](#system-overview)  
4. [Tech Stack](#tech-stack)  
5. [Setup & Installation](#setup--installation)  
6. [Environment Variables](#environment-variables)  
7. [API Endpoints](#api-endpoints)  
8. [Running the Backend](#running-the-backend)  
9. [Testing](#testing)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## 🌟 **Introduction**  

The **StartifyAI Backend** serves as the brain of the application, managing API requests, performing data validation, querying vector databases, and interacting with AI models for health checks, global queries, and pitch deck generation.

---

## 🛠️ **Features**  

### ✅ **1. Global Query Processing**  
- Accepts user queries.  
- Retrieves relevant data from **Pinecone Vector DB**.  
- Augments the query with context and processes it via **OpenAI GPT**.  

### ✅ **2. Startup Health Check API**  
- Compares user-provided financial metrics with pre-defined benchmarks.  
- Provides health analysis using LLM-generated summaries.  

### ✅ **3. Pitch Deck Generation**  
- Accepts startup information (e.g., name, problem statement, founders).  
- Generates a detailed pitch deck using **OpenAI GPT**.  

### ✅ **4. Authentication Integration**  
- Handles secure routes and validates user sessions using **Clerk API**.  

---

## 🧠 **System Overview**  

```plaintext
+-----------------------------------------------+
|              Backend Service                 |
+-----------------------------------------------+
| Routes: FastAPI                               |
|  - /api/query                                 |
|  - /api/health_check                          |
|  - /api/pitch_deck                            |
+-----------------------------------------------+
| Services                                      |
|  - Query Service                              |
|  - Health Check Service                       |
|  - Pitch Deck Service                         |
+-----------------------------------------------+
| Integrations                                  |
|  - Pinecone (Vector Database)                 |
|  - OpenAI GPT (LLM)                           |
|  - Clerk (Authentication)                     |
+-----------------------------------------------+
| Data Models                                   |
|  - Health Check Benchmarks                    |
|  - Pitch Deck Template                        |
+-----------------------------------------------+
| Database: Vector DB (Pinecone)                |
+-----------------------------------------------+
```

---

## 💻 **Tech Stack**  

- **Backend Framework:** FastAPI  
- **Language:** Python 3.9+
- **Language:** MongoDB
- **Vector Database:** Pinecone  
- **AI Model:** OpenAI GPT (3.5/4)  
- **Authentication:** Clerk  


---

## 📊 **API Endpoints**  

### ✅ **1. Global Query Search**  
- **Endpoint:** `POST /api/query`  
- **Description:** Processes user query and retrieves insights.  

### ✅ **2. Startup Health Check**  
- **Endpoint:** `POST /api/health_check`  
- **Description:** Compares financial metrics with benchmarks.  
- **Request Body Example:**  

### ✅ **3. Pitch Deck Generator**  
- **Endpoint:** `POST /api/pitch_deck`  
- **Description:** Generates a pitch deck based on startup details.  
- **Request Body Example:**  

---

Let’s build smarter startups with AI! 🚀✨
