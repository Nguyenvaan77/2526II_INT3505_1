"""
Test script for Library Management API

This script demonstrates how to test the API with different tools
and methods generated from the API documentation formats.
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:3000"
HEADERS = {"Content-Type": "application/json"}


class LibraryAPITester:
    """Test suite for Library Management API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.created_book_id = None
    
    def print_response(self, response: requests.Response, test_name: str):
        """Pretty print response"""
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        try:
            print(f"Body:\n{json.dumps(response.json(), indent=2)}")
        except:
            print(f"Body:\n{response.text}")
    
    def test_get_all_books(self):
        """Test: Get all books"""
        response = self.session.get(
            f"{self.base_url}/books",
            headers=HEADERS
        )
        self.print_response(response, "GET /books - Get all books")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        print("✅ PASSED: Get all books")
    
    def test_get_all_books_with_pagination(self):
        """Test: Get all books with pagination"""
        response = self.session.get(
            f"{self.base_url}/books",
            params={"skip": 0, "limit": 1},
            headers=HEADERS
        )
        self.print_response(response, "GET /books?skip=0&limit=1 - With pagination")
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        assert data["limit"] == 1
        print("✅ PASSED: Get books with pagination")
    
    def test_get_all_books_sorted(self):
        """Test: Get all books with sorting"""
        response = self.session.get(
            f"{self.base_url}/books",
            params={"sort_by": "name"},
            headers=HEADERS
        )
        self.print_response(response, "GET /books?sort_by=name - Sorted by name")
        assert response.status_code == 200
        print("✅ PASSED: Get books sorted")
    
    def test_create_book(self):
        """Test: Create a new book"""
        payload = {
            "name": "The Pragmatic Programmer",
            "author_name": "Andrew Hunt & David Thomas",
            "description": "Hướng dẫn thực hành lập trình kỹ thuật"
        }
        response = self.session.post(
            f"{self.base_url}/books",
            json=payload,
            headers=HEADERS
        )
        self.print_response(response, "POST /books - Create new book")
        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert data["data"]["name"] == payload["name"]
        self.created_book_id = data["data"]["id"]
        print("✅ PASSED: Create book")
    
    def test_create_book_invalid(self):
        """Test: Create book with invalid data"""
        payload = {
            "name": "Test Book"
            # Missing author_name and description
        }
        response = self.session.post(
            f"{self.base_url}/books",
            json=payload,
            headers=HEADERS
        )
        self.print_response(response, "POST /books - Invalid request (missing fields)")
        assert response.status_code == 400
        data = response.json()
        assert "details" in data
        print("✅ PASSED: Validation error handling")
    
    def test_get_book(self):
        """Test: Get a single book"""
        if not self.created_book_id:
            book_id = "1"
        else:
            book_id = self.created_book_id
        
        response = self.session.get(
            f"{self.base_url}/books/{book_id}",
            headers=HEADERS
        )
        self.print_response(response, f"GET /books/{book_id} - Get single book")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == book_id
        print("✅ PASSED: Get single book")
    
    def test_get_book_not_found(self):
        """Test: Get non-existent book"""
        response = self.session.get(
            f"{self.base_url}/books/999999",
            headers=HEADERS
        )
        self.print_response(response, "GET /books/999999 - Book not found")
        assert response.status_code == 404
        print("✅ PASSED: 404 error handling")
    
    def test_update_book(self):
        """Test: Update a book"""
        if not self.created_book_id:
            book_id = "1"
        else:
            book_id = self.created_book_id
        
        payload = {
            "name": "The Pragmatic Programmer - Updated Edition",
            "description": "Phiên bản cập nhật với thêm nhiều tư vấn thực tế"
        }
        response = self.session.put(
            f"{self.base_url}/books/{book_id}",
            json=payload,
            headers=HEADERS
        )
        self.print_response(response, f"PUT /books/{book_id} - Update book")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == payload["name"]
        print("✅ PASSED: Update book")
    
    def test_delete_book(self):
        """Test: Delete a book"""
        if not self.created_book_id:
            book_id = "2"  # Use an existing book for testing
        else:
            book_id = self.created_book_id
        
        response = self.session.delete(
            f"{self.base_url}/books/{book_id}",
            headers=HEADERS
        )
        self.print_response(response, f"DELETE /books/{book_id} - Delete book")
        assert response.status_code == 200
        print("✅ PASSED: Delete book")
    
    def test_delete_book_not_found(self):
        """Test: Delete non-existent book"""
        response = self.session.delete(
            f"{self.base_url}/books/999999",
            headers=HEADERS
        )
        self.print_response(response, "DELETE /books/999999 - Delete non-existent book")
        assert response.status_code == 404
        print("✅ PASSED: Delete error handling")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("🧪 Running Library Management API Tests")
        print("="*60)
        
        tests = [
            self.test_get_all_books,
            self.test_get_all_books_with_pagination,
            self.test_get_all_books_sorted,
            self.test_create_book,
            self.test_create_book_invalid,
            self.test_get_book,
            self.test_get_book_not_found,
            self.test_update_book,
            self.test_delete_book,
            self.test_delete_book_not_found,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                passed += 1
            except Exception as e:
                print(f"❌ FAILED: {e}")
                failed += 1
        
        print("\n" + "="*60)
        print(f"📊 Test Results: {passed} passed, {failed} failed")
        print("="*60)


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/books")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running at", BASE_URL)
        print("💡 Please start the server first with: python app.py")
        exit(1)
    
    # Run tests
    tester = LibraryAPITester()
    tester.run_all_tests()
