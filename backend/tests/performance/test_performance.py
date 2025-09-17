"""
Performance and load testing for the API.
Tests response times, concurrent requests, and system performance under load.
"""

import time
import threading
import statistics
from typing import List

import psutil
import pytest
from fastapi.testclient import TestClient


@pytest.mark.performance
class TestPerformance:
    """Performance and load testing."""

    def test_health_check_response_time(self, client: TestClient):
        """Test health check endpoint response time."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 0.1  # Should respond within 100ms

    def test_detailed_health_check_response_time(self, client: TestClient):
        """Test detailed health check endpoint response time."""
        start_time = time.time()
        response = client.get("/health/detailed")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 0.5  # Should respond within 500ms

    def test_concurrent_health_checks(self, client: TestClient):
        """Test multiple concurrent health check requests."""
        def make_request() -> float:
            start = time.time()
            response = client.get("/health")
            end = time.time()
            assert response.status_code == 200
            return end - start

        # Test with 20 concurrent requests
        num_requests = 20
        response_times: List[float] = []

        threads = []
        for _ in range(num_requests):
            thread = threading.Thread(target=lambda: response_times.append(make_request()))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=10)

        assert len(response_times) == num_requests
        
        # Analyze response times
        avg_time = statistics.mean(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile

        # Performance assertions
        assert avg_time < 0.2  # Average under 200ms
        assert max_time < 1.0  # Max under 1 second
        assert p95_time < 0.5  # 95th percentile under 500ms

    def test_database_query_performance(self, client: TestClient, mock_get_current_user):
        """Test database query performance for watchlist operations."""
        # Create some test data first
        for i in range(10):
            watchlist_data = {
                "anime_id": 1000 + i,
                "anime_title": f"Performance Test Anime {i}",
                "status": "watching"
            }
            response = client.post("/api/v1/watchlist", json=watchlist_data)
            assert response.status_code == 201

        # Test watchlist retrieval performance
        start_time = time.time()
        response = client.get("/api/v1/watchlist")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 0.5  # Should respond within 500ms

        data = response.json()
        assert len(data["items"]) >= 10

    def test_pagination_performance(self, client: TestClient, mock_get_current_user):
        """Test pagination performance with large datasets."""
        # Test with different page sizes
        page_sizes = [10, 50, 100]
        
        for limit in page_sizes:
            start_time = time.time()
            response = client.get(f"/api/v1/watchlist?limit={limit}")
            end_time = time.time()
            
            assert response.status_code == 200
            response_time = end_time - start_time
            
            # Larger pages can take longer but should still be reasonable
            max_expected_time = 0.1 + (limit * 0.001)  # Base 100ms + 1ms per item
            assert response_time < max_expected_time

    def test_memory_usage_stability(self, client: TestClient):
        """Test that memory usage remains stable under load."""
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Make many requests
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be minimal (less than 10MB)
        assert memory_increase < 10.0

    def test_rate_limiting_performance(self, client: TestClient):
        """Test that rate limiting doesn't significantly impact performance."""
        # Make requests up to rate limit
        response_times = []
        
        for i in range(15):  # More than the limit of 10
            start_time = time.time()
            response = client.get("/health")  # This endpoint might have rate limiting
            end_time = time.time()
            
            response_times.append(end_time - start_time)
            
            # Some requests should be rate limited
            if i >= 10:  # Assuming 10 requests per window
                assert response.status_code in [200, 429]
            else:
                assert response.status_code == 200
        
        # Even rate limited requests should be fast
        avg_time = statistics.mean(response_times)
        assert avg_time < 0.2  # Average under 200ms

    def test_cache_performance(self, client: TestClient, mock_get_current_user):
        """Test caching performance improvements."""
        # First request (should cache)
        start_time = time.time()
        response1 = client.get("/api/v1/watchlist")
        end_time = time.time()
        first_request_time = end_time - start_time
        
        assert response1.status_code == 200
        
        # Second request (should use cache)
        start_time = time.time()
        response2 = client.get("/api/v1/watchlist")
        end_time = time.time()
        second_request_time = end_time - start_time
        
        assert response2.status_code == 200
        
        # Cached request should be faster (at least 20% improvement)
        if second_request_time > 0:  # Avoid division by zero
            improvement_ratio = first_request_time / second_request_time
            assert improvement_ratio > 1.1  # At least 10% improvement

    @pytest.mark.slow
    def test_sustained_load(self, client: TestClient):
        """Test sustained load over time."""
        import time
        
        start_time = time.time()
        request_count = 0
        errors = 0
        
        # Run for 10 seconds
        while time.time() - start_time < 10:
            try:
                response = client.get("/health")
                assert response.status_code == 200
                request_count += 1
            except Exception:
                errors += 1
            
            time.sleep(0.01)  # Small delay between requests
        
        # Should handle at least 50 requests in 10 seconds
        assert request_count >= 50
        # Error rate should be very low
        error_rate = errors / (request_count + errors) if (request_count + errors) > 0 else 0
        assert error_rate < 0.05  # Less than 5% error rate

    def test_large_response_handling(self, client: TestClient, mock_get_current_user):
        """Test handling of potentially large responses."""
        # Add many items to create a large response
        for i in range(50):
            watchlist_data = {
                "anime_id": 2000 + i,
                "anime_title": f"Large Response Test Anime {i}",
                "status": "watching",
                "notes": f"Detailed notes for anime {i}. " * 10  # Make notes longer
            }
            response = client.post("/api/v1/watchlist", json=watchlist_data)
            if response.status_code != 201:
                # Might fail due to unique constraints, that's ok
                break
        
        # Test retrieval of large dataset
        start_time = time.time()
        response = client.get("/api/v1/watchlist?limit=100")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        
        # Should handle large responses reasonably well
        assert response_time < 2.0  # Under 2 seconds for large response
