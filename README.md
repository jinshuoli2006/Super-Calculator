# Super Math Suite 2025

A modern, modular Python application for advanced mathematics, built with PyQt6 and NumPy.

## Features

1.  **Scientific Calculator**: Supports standard operations and math functions (sin, cos, log, etc.).
2.  **Linear Algebra**: Create matrices, calculate Determinants, RREF, Inverse, Rank, and Transpose.
3.  **Graph Theory (Interactive)**: 
    - Draw nodes and edges on a canvas.
    - Toggle between Directed and Undirected graphs.
    - Export the visual graph to an Adjacency Matrix (Python List format).
4.  **Calculus & Plotting**:
    - Add multiple functions (e.g., `x**2`, `np.sin(x)`).
    - Dynamic plotting using Matplotlib integration.

## Installation

1.  **Install Python 3.9+**
2.  **Install Dependencies**:
    ```bash
    pip install PyQt6 matplotlib numpy networkx sympy
    ```
    *(Note: `sympy` is optional but recommended for better RREF precision).*

## How to Run

1.  Navigate to the project folder.
2.  Run the main script:
    ```bash
    python main.py
    ```

## Usage Guide

### Graph Theory Module
The Graph module has been updated for better usability:

1.  Select **"Add Node"**: Click anywhere on the white canvas to create a node.
2.  Select **"Add Edge"**:
    - **Click** the Source Node (it will turn Orange).
    - **Click** the Destination Node.
    - Enter the **Weight** in the popup dialog.
3.  **Directed/Undirected**: Use the checkbox to switch modes. Directed edges show an arrow.
4.  **Generate Matrix**: Click the button to get the Python-compatible list representation of your drawn graph.

### Calculus Module
- Enter functions using Python syntax (e.g., `x**2`, `np.exp(x)`).
- Click "+" to add more functions to compare them on the same plot.
