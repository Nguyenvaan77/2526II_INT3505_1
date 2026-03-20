"""
Library Management API - Python Flask Implementation
Generated from OpenAPI, API Blueprint, RAML, and TypeSpec

This is a simple implementation of the Library Management API
using Python Flask framework.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import uuid

app = Flask(__name__)

# In-memory database (in production, use actual database)
books_db = [
    {
        "id": "1",
        "name": "Clean Code",
        "author_name": "Robert C. Martin",
        "description": "Hướng dẫn viết code sạch",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-20T15:45:00Z"
    },
    {
        "id": "2",
        "name": "Design Patterns",
        "author_name": "Gang of Four",
        "description": "Sách về các design pattern",
        "created_at": "2024-01-16T11:00:00Z",
        "updated_at": "2024-01-21T16:00:00Z"
    }
]


# Helper function to validate book data
def validate_book(data):
    """Validate book data"""
    errors = []
    
    if not data.get('name'):
        errors.append("name is required")
    elif not isinstance(data.get('name'), str) or len(data['name']) == 0:
        errors.append("name must be a non-empty string")
    elif len(data['name']) > 255:
        errors.append("name must not exceed 255 characters")
    
    if not data.get('author_name'):
        errors.append("author_name is required")
    elif not isinstance(data.get('author_name'), str) or len(data['author_name']) == 0:
        errors.append("author_name must be a non-empty string")
    elif len(data['author_name']) > 255:
        errors.append("author_name must not exceed 255 characters")
    
    if not data.get('description'):
        errors.append("description is required")
    elif not isinstance(data.get('description'), str):
        errors.append("description must be a string")
    elif len(data.get('description', '')) > 1000:
        errors.append("description must not exceed 1000 characters")
    
    return errors


# Route: Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    """
    Get all books with pagination
    Query parameters:
    - skip: int (default: 0) - Number of books to skip
    - limit: int (default: 10) - Number of books to return
    - sort_by: str (default: 'created_at') - Sort by field
    """
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        sort_by = request.args.get('sort_by', 'created_at')
        
        # Validation
        if skip < 0:
            skip = 0
        if limit < 1:
            limit = 10
        
        # Sort
        sorted_books = books_db.copy()
        if sort_by in ['name', 'author_name', 'created_at']:
            sorted_books.sort(key=lambda x: x.get(sort_by, ''))
        
        # Paginate
        paginated = sorted_books[skip:skip + limit]
        
        return jsonify({
            "data": paginated,
            "total": len(books_db),
            "skip": skip,
            "limit": limit
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500


# Route: Create a book
@app.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    Request body:
    {
        "name": string (required),
        "author_name": string (required),
        "description": string (required)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request",
                "status": 400,
                "details": ["Request body must be JSON"]
            }), 400
        
        # Validate
        errors = validate_book(data)
        if errors:
            return jsonify({
                "error": "Invalid request",
                "status": 400,
                "details": errors
            }), 400
        
        # Create new book
        new_book = {
            "id": str(uuid.uuid4()),
            "name": data['name'],
            "author_name": data['author_name'],
            "description": data['description'],
            "created_at": datetime.utcnow().isoformat() + 'Z',
            "updated_at": datetime.utcnow().isoformat() + 'Z'
        }
        
        books_db.append(new_book)
        
        return jsonify({
            "data": new_book,
            "message": "Book created successfully"
        }), 201
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500


# Route: Get one book
@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    """Get a book by ID"""
    try:
        for book in books_db:
            if book['id'] == id:
                return jsonify({"data": book}), 200
        
        return jsonify({
            "error": "Book not found",
            "status": 404
        }), 404
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500


# Route: Update a book
@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    """
    Update a book
    Request body: (all fields optional)
    {
        "name": string,
        "author_name": string,
        "description": string
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request",
                "status": 400,
                "details": ["Request body must be JSON"]
            }), 400
        
        # Find book
        book = None
        for b in books_db:
            if b['id'] == id:
                book = b
                break
        
        if not book:
            return jsonify({
                "error": "Book not found",
                "status": 404
            }), 404
        
        # Update fields
        if 'name' in data and data['name']:
            if not isinstance(data['name'], str) or len(data['name']) == 0:
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["name must be a non-empty string"]
                }), 400
            if len(data['name']) > 255:
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["name must not exceed 255 characters"]
                }), 400
            book['name'] = data['name']
        
        if 'author_name' in data and data['author_name']:
            if not isinstance(data['author_name'], str) or len(data['author_name']) == 0:
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["author_name must be a non-empty string"]
                }), 400
            if len(data['author_name']) > 255:
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["author_name must not exceed 255 characters"]
                }), 400
            book['author_name'] = data['author_name']
        
        if 'description' in data and data['description']:
            if not isinstance(data['description'], str):
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["description must be a string"]
                }), 400
            if len(data['description']) > 1000:
                return jsonify({
                    "error": "Invalid request",
                    "status": 400,
                    "details": ["description must not exceed 1000 characters"]
                }), 400
            book['description'] = data['description']
        
        book['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        
        return jsonify({
            "data": book,
            "message": "Book updated successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500


# Route: Delete a book
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    """Delete a book by ID"""
    try:
        # Find and remove book
        for i, book in enumerate(books_db):
            if book['id'] == id:
                books_db.pop(i)
                return jsonify({
                    "message": "Book deleted successfully"
                }), 200
        
        return jsonify({
            "error": "Book not found",
            "status": 404
        }), 404
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found",
        "status": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500


if __name__ == '__main__':
    print("🚀 Library Management API Server")
    print("📚 Starting on http://localhost:3000")
    print("🔗 Use: GET /books, POST /books, GET /books/{id}, PUT /books/{id}, DELETE /books/{id}")
    app.run(debug=True, port=3000, host='0.0.0.0')
