#!/usr/bin/env python3
"""Python script that provides some stats about Nginx
logs stored in MongoDB"""
from pymongo import MongoClient

def main():
    """Connect to MongoDB"""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    """Count total logs"""
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    """Count methods"""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")

    """Count specific GET request"""
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    main()
