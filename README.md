# Library-Management-System

A simple library management system built using Python and Tkinter for the graphical user interface (GUI). This application allows users to manage books, including adding, deleting, issuing, and returning books. It also supports viewing available books and the list of issued books.

### Features

- **Add a Book**: Adds a new book to the library.
- **Delete a Book**: Removes a book from the library.
- **Issue a Book**: Issues a book to a student.
- **Return a Book**: Returns an issued book to the library.
- **View Books**: Displays a list of all available books in the library.
- **Issued Books**: Displays a list of books that have been issued, along with the student's name, ID and date of issuing.

### Installation

Set up two MySQL tables: one to store all the books and one to store details about issued books.\

```sql
CREATE TABLE books (
    bid VARCHAR(20) PRIMARY KEY,
    title VARCHAR(30),
    author VARCHAR(30),
    status VARCHAR(30)
);

CREATE TABLE books_issued (
    bid VARCHAR(20) PRIMARY KEY,
    student_name VARCHAR(30),
    student_id VARCHAR(20),
    date date
);
```
