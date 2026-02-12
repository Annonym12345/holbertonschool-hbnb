# Git Intro Project

# HBnB Project - Architecture Documentation

## Overview
This repository contains the architectural documentation for the HBnB application. It provides a detailed overview of the system's structure, business logic, and API interactions through diagrams and explanatory notes.

The documentation includes:

- **High-Level Package Diagram** (Task 0)
- **Business Logic Layer Class Diagram** (Task 1)
- **Sequence Diagrams for API Calls** (Task 2)

These diagrams and notes serve as a blueprint for the implementation and development of HBnB.

---

## File Structure

.
├── README.md
├── explication0.md # High-Level Package Diagram
├── explication1.md # Business Logic Layer Class Diagram
├── explication2.md # Sequence Diagrams for API Calls


---

## Task 0 – High-Level Package Diagram

- Shows the three-layer architecture:
  - **Presentation Layer** (API / Services)
  - **Business Logic Layer** (Domain Models)
  - **Persistence Layer** (Repositories / Database)
- Demonstrates the use of the **HBnB Facade** for simplifying interactions between layers.
- Explains communication pathways for requests and data operations.

Refer to `note0.md` for the diagram and detailed explanations.

---

## Task 1 – Business Logic Layer Class Diagram

- Represents the main entities of the system:
  - **User**
  - **Place**
  - **Review**
  - **Amenity**
- Shows attributes, methods, and relationships:
  - User owns Places and writes Reviews
  - Place has Reviews and includes Amenities
- Highlights business rules encapsulated in models.

Refer to `note1.md` for the class diagram and details.

---

## Task 2 – Sequence Diagrams for API Calls

- Illustrates the flow of information across layers for API calls:
  - User Registration
  - Place Creation
  - Review Submission
  - Fetching List of Places
- Shows the interaction between:
  - **Presentation Layer** (API / Services)
  - **Business Logic Layer** (Domain Models)
  - **Persistence Layer** (Repositories / Database)
- Demonstrates CRUD operations and the role of the **facade**.

Refer to `note2.md` for the sequence diagrams and explanations.

---

## Usage

1. Open the `.md` files (`note0.md`, `note1.md`, `note2.md`) in a Markdown editor that supports **Mermaid diagrams** (e.g., VSCode with Mermaid plugin, Obsidian, GitHub web viewer).
2. Visualize the architecture, class, and sequence diagrams directly.
3. Use this documentation as a reference during development to understand:
   - Layered architecture
   - Entity relationships
   - API request flow

---

---

## Notes

- Diagrams are simplified for clarity and focus on core components.
- All UUIDs, timestamps, and key attributes/methods are included in the class diagrams.
- Sequence diagrams demonstrate typical user interactions with the HBnB system.

---

## Author

Holberton School HBnB Project Team
