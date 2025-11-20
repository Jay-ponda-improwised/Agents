#!/usr/bin/env python3
"""
Test script for the new Input component.
"""

import sys
import os

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utility.Console.VirtualMarkdownBoard import VirtualMarkdownBoard


def test_input_component():
    """Test the new Input component."""
    print("Testing Input Component")
    print("=" * 30)
    
    # Create a new board
    board = VirtualMarkdownBoard()
    
    # Add some components to demonstrate the input component
    board.main_title("Input Component Demo")
    board.sub_title("This demonstrates the new input functionality")
    board.n()
    
    # Add the input component
    # Note: This will pause execution to get user input
    board.input("Please enter your name")
    board.n()
    
    # Add another input for password
    board.input("Enter a secret password", password=True)
    board.n()
    
    # Display everything
    board.take_snapshot("Input Component Test")


if __name__ == "__main__":
    test_input_component()