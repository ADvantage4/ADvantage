from trend_summarizer_agent import summarizer

# Sample test data
TEST_TREND = "PBKS vs LSG IPL Match"
TEST_CONTENT = """
• Punjab Kings defeated Lucknow Super Giants by 5 wickets
• Match played on May 4th at Ekana Stadium
• Shikhar Dhawan scored 70 runs
• Arshdeep Singh took 3 wickets
• Attendance: 45,000 fans
"""

if __name__ == "__main__":
    print("Testing Trend Summarizer...")
    print(f"Trend: {TEST_TREND}")
    print("Generating summary...\n")
    
    result = summarizer.summarize_trend(TEST_TREND, TEST_CONTENT)
    
    print("=== SUMMARY RESULT ===")
    print(result)
    print("\nTest completed.")