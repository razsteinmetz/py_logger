"""
Multi-file project example using PyLogger.

This example demonstrates how to use PyLogger across multiple modules
in a larger project with centralized configuration.
"""

import os
import sys
sys.path.insert(0, 'c:/Users/raz/OneDrive - Sage/Pycharm/PycharmProjects/py_logger')

from py_logger import PyLogger

# Global logger configuration
LOGGER_CONFIG = {
    "console": {
        "enabled": True,
        "level": "INFO",
        "format": "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s"
    },
    "file": {
        "enabled": True,
        "level": "DEBUG",
        "filename": "multifile_example.log",
        "max_size": 1048576,  # 1MB
        "backup_count": 3,
        "format": "%(asctime)s | %(name)-12s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s"
    }
}

# Global logger instance
_app_logger = None

def initialize_logger(name="MultiFileApp"):
    """Initialize the PyLogger instance once at application startup."""
    global _app_logger
    if _app_logger is None:
        _app_logger = PyLogger(config=LOGGER_CONFIG, name=name)
    return _app_logger

def get_logger():
    """Get the initialized PyLogger instance."""
    if _app_logger is None:
        raise RuntimeError("Logger not initialized. Call initialize_logger() first.")
    return _app_logger

# Simulate different modules

class DatabaseManager:
    """Database management module."""
    
    def __init__(self):
        self.logger = get_logger()
        self.logger.debug("DatabaseManager initialized")
        self.connected = False
    
    def connect(self):
        self.logger.info("Connecting to database...")
        try:
            # Simulate database connection
            self.connected = True
            self.logger.info("Database connected successfully")
            return True
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return False
    
    def execute_query(self, query):
        if not self.connected:
            self.logger.warning("Database not connected, cannot execute query")
            return None
        
        self.logger.debug(f"Executing query: {query}")
        # Simulate query execution
        result = f"Result for: {query}"
        self.logger.debug("Query executed successfully")
        return result

class APIHandler:
    """API handling module."""
    
    def __init__(self):
        self.logger = get_logger()
        self.logger.debug("APIHandler initialized")
        self.server_running = False
    
    def start_server(self):
        self.logger.info("Starting API server...")
        self.server_running = True
        self.logger.info("API server started on port 8080")
    
    def handle_request(self, endpoint, data=None):
        self.logger.info(f"Handling request to {endpoint}")
        
        try:
            # Simulate request processing
            if endpoint == "/error":
                raise ValueError("Simulated API error")
            
            response = {"status": "success", "endpoint": endpoint, "data": data}
            self.logger.debug(f"Request processed successfully: {response}")
            return response
            
        except Exception as e:
            self.logger.error(f"Request failed for {endpoint}: {e}")
            return {"status": "error", "message": str(e)}

class BusinessLogic:
    """Business logic module."""
    
    def __init__(self, db_manager):
        self.logger = get_logger()
        self.db = db_manager
        self.logger.debug("BusinessLogic initialized")
    
    def process_user_data(self, user_id, data):
        self.logger.info(f"Processing data for user {user_id}")
        
        try:
            # Validate data
            if not data:
                self.logger.warning(f"No data provided for user {user_id}")
                return None
            
            # Save to database
            query = f"INSERT INTO users (id, data) VALUES ({user_id}, '{data}')"
            result = self.db.execute_query(query)
            
            if result:
                self.logger.info(f"User data processed successfully for user {user_id}")
                return {"user_id": user_id, "status": "processed"}
            else:
                self.logger.error(f"Failed to save data for user {user_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error processing user data: {e}")
            return None
    
    def send_notification(self, message, urgent=False):
        """Send notifications through the logger."""
        self.logger.info(f"Sending notification: {message}")
        
        if urgent:
            # This would send immediate notifications if configured
            self.logger.error(f"URGENT: {message}")
        else:
            self.logger.info(f"INFO: {message}")

def main():
    """Main application function."""
    # Initialize logger once at startup
    main_logger = initialize_logger("MultiFileApp")
    main_logger.info("=" * 50)
    main_logger.info("Multi-File Project Example Starting")
    main_logger.info("=" * 50)
    
    # Initialize components
    db = DatabaseManager()
    api = APIHandler()
    business = BusinessLogic(db)
    
    # Start services
    main_logger.info("Initializing application components...")
    
    if not db.connect():
        main_logger.critical("Failed to connect to database - shutting down")
        return False
    
    api.start_server()
    
    # Simulate application workflow
    main_logger.info("Processing sample requests...")
    
    # Successful API requests
    response1 = api.handle_request("/users", {"name": "John Doe"})
    response2 = api.handle_request("/data", {"value": 123})
    
    # Process business logic
    result1 = business.process_user_data(1, "User data 1")
    result2 = business.process_user_data(2, "User data 2")
    result3 = business.process_user_data(3, "")  # Empty data - will cause warning
    
    # Simulate error condition
    main_logger.info("Simulating error condition...")
    error_response = api.handle_request("/error")
    
    # Send some notifications
    business.send_notification("Daily processing completed")
    business.send_notification("System error detected", urgent=True)
    
    # Application shutdown
    main_logger.info("Application processing completed")
    main_logger.info("=" * 50)
    
    # Show log file information
    if os.path.exists("multifile_example.log"):
        with open("multifile_example.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
            main_logger.info(f"Log file contains {len(lines)} entries")
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\nApplication completed: {'Successfully' if success else 'With errors'}")
    print("Check 'multifile_example.log' for detailed logs from all modules.")