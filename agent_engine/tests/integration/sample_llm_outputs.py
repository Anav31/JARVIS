"""
===============================================================================
File Name   : sample_llm_outputs.py
Module      : Integration Tests
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Contains sample LLM outputs used for end-to-end pipeline testing.

These simulate the JSON responses received from the LLM Team before entering
the Agent Brain.

Author : Team JARVIS
===============================================================================
"""

# =============================================================================
# Test Case 1
# =============================================================================

SPRING_AI_CASE = {
    "goal": "Summarize the latest PDF of Spring AI tutorial",
    "summary": (
        "Open browser, perform search for Spring AI tutorial, "
        "download the latest PDF and summarize it."
    ),
    "missing_information": [
        "URL or specific source for Spring AI tutorial"
    ],
    "tasks": [
        "Open Chrome",
        "Search for Spring AI tutorial URL",
        "Navigate to the found URL",
        "Download the latest PDF available",
        "Summarize the downloaded PDF"
    ]
}
'''
# =============================================================================
# Test Case 2
# =============================================================================

MOVIE_BOOKING_CASE = {
    "goal": (
        "Complete the pending feature of Movie Booking microservices "
        "project and prepare a summary of changes."
    ),
    "summary": (
        "Resume work on Movie Booking microservice, complete pending "
        "feature, review existing implementation, run application, "
        "execute tests, and prepare summary of changes."
    ),
    "missing_information": [
        "Identify the pending feature"
    ],
    "tasks": [
        "Identify pending feature",
        "Open VS Code",
        "Navigate to Movie Booking microservice",
        "Review existing implementation",
        "Complete remaining work on identified feature",
        "Run the application",
        "Execute all tests",
        "Prepare a summary of changes"
    ]
}

# =============================================================================
# Test Case 3
# =============================================================================

PRESENTATION_CASE = {
    "goal": (
        "Prepare a five-minute presentation on the comparison of "
        "multimodal large language models and Attention Is All You Need."
    ),
    "summary": (
        "Find, download, read, compare, generate report, create "
        "PowerPoint presentation, and prepare script for a presentation."
    ),
    "missing_information": [
        "Browser to use for research",
        "Location of the latest research paper on multimodal large language models"
    ],
    "tasks": [
        "Search for the latest research paper on multimodal large language models",
        "Determine location of the downloadable version of the research paper",
        "Download the research paper",
        "Read every section of the research paper",
        "Compare it with the paper 'Attention Is All You Need'",
        "Identify the main architectural differences",
        "Generate a detailed comparison report",
        "Create a PowerPoint presentation with diagrams",
        "Prepare a five-minute presentation script"
    ]
}'''

# =============================================================================
# All Test Cases
# =============================================================================

ALL_CASES = [
    SPRING_AI_CASE]