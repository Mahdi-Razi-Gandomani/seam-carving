# 🪄 Seam Carving — Content-Aware Image Resizing

## 📘 Overview
This project implements **content-aware image resizing** using **seam carving**, a technique that intelligently removes pixels from an image while preserving its most important visual content.  

Two methods are used for finding seams:
- **Dijkstra’s Algorithm** — a graph-based approach using shortest path computation.  
- **Dynamic Programming** — an optimized method that reduces computation time. 

| Original Image | Simple Cropping | Seam Carving |
|----------------|-----------------|---------------|
| ![original](data/input1.jpg) | ![crop](data/cropped_input1.jpg) | ![seam](data/output1.jpg) |

### 🧪 Example Visuals

Below are examples showing the seam removal process.

![Seam Carving Test](data/output1_process.gif)

![Seam Carving Test](data/output2_process.gif)

---

## 🧩 File Description

| File / Directory | Description |
|------------------|-------------|
| `graph.py` | Defines the `Graph` interface and `Edge` class for graph representation. |
| `dijkstra.py` | Implements Dijkstra’s algorithm (`DijkstraShortestPathFinder`) and the graph reduction for seam finding (`DijkstraMethod`). |
| `dynamic_programming.py` | Implements the dynamic programming seam finder (`DpMethod`). |
| `utilities.py` | Includes the energy function, seam removal utilities, and image manipulation functions. |
| `visualization.py` | Provides utilities to visualize seams and create animated GIFs. |
| `cli.py` | Command-line interface for running seam carving directly. |
| `main.py` | Entry point of the project. Runs the CLI and manages input/output. |
| `data/` | Contains example input images and expected outputs for testing. |

---

## ⚙️ Getting Started

### 📦 Clone the Repository
```bash
git clone https://github.com/mahdi-razi-gandomani/seam-carving.git
cd seam-carving
```

### ▶️ Running the Program
You can run the seam carving tool directly from the command line:

```bash
python3 main.py data/input2.jpg data/output2.jpg --vertical 50 --horizontal 30 --method dp --gif
```

### 🧠 CLI Arguments

| Argument | Description | Default |
|-----------|-------------|----------|
| `input` | Input image file | — |
| `output` | Output image file | — |
| `--vertical` | Number of vertical seams to remove | `0` |
| `--horizontal` | Number of horizontal seams to remove | `0` |
| `--method` | Seam finding method (`dp` or `dijkstra`) | `dp` |
| `--gif` | Generate GIF showing seam removal | `False` |

---

## 🧮 How It Works

### 🖼️ What Is Seam Carving?
Seam carving is a **content-aware image resizing** algorithm that removes (or inserts) seams — connected paths of least “energy” pixels — from an image.  
Instead of cropping edges or uniformly scaling, it preserves the most visually important regions.

### ⚡ Energy Function
The **energy function** estimates the “importance” of each pixel based on local gradients:

$$
E(x, y) = \sqrt{(dR_x^2 + dG_x^2 + dB_x^2) + (dR_y^2 + dG_y^2 + dB_y^2)}
$$

High energy = significant detail (edges, objects)  
Low energy = background or uniform areas



### 🧭 Finding Seams via Dijkstra’s Algorithm
1. Model the image as a **directed acyclic graph (DAG)**:
   - Pixels → vertices  
   - Energy values → edge weights  
   - Adjacent pixels → directed edges
2. Use **Dijkstra’s algorithm** to find the lowest-energy path (shortest path).
3. Remove that path (seam) from the image.

### 💡 Dynamic Programming Alternative
The DP method computes minimum-energy paths more efficiently by reusing results from previous columns/rows, achieving better runtime with less memory overhead.
