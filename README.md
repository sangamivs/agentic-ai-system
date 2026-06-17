# Customer Support Agent with RAG

## Project Overview

Customer Support Agent is an Agentic AI project that answers customer queries using Retrieval-Augmented Generation (RAG).

The goal is to build an intelligent support system that can retrieve information from company documents and generate accurate, context-aware responses using local LLMs.

---

# Day 1 Progress

## Agentic AI Fundamentals

Completed:

* Agentic AI Theory
* ReAct Pattern
* Plan-and-Execute Pattern
* Multi-Agent Systems
* LangChain Basics
* LangGraph Basics
* CrewAI Basics
* RAG Fundamentals

---

## Environment Setup

Installed:

* Python 3.14.5
* Docker
* Ollama
* LangChain
* LangGraph
* ChromaDB
* FastAPI

---

## Project Initialization

Completed:

* Git Initialization
* GitHub Repository Setup
* Project Scaffold Creation

Project Folder:

```text
agentic-ai-system
```

---

# Day 2 Progress

## Model Selection Framework

Models were evaluated using:

* Task Capability
* Context Window
* Latency
* Cost
* Privacy

---

## OSS Model Families Studied

* Llama 3.1
* Qwen 2.5
* Mistral 7B
* Gemma
* DeepSeek
* Phi-3

---

## Quantization

Learned:

### Q4_K_M

* Lower memory usage
* Faster inference
* Recommended for development

### Q8_0

* Better quality
* Higher memory requirements

### F16

* Full precision
* Highest memory requirements

---

## Model Comparison

### Llama 3.1 8B

Strengths:

* Excellent instruction following
* Strong RAG performance
* Recommended production model

---

### Qwen 2.5 7B

Strengths:

* Strong reasoning
* Strong coding capability
* Good multilingual support

---

### Mistral 7B

Strengths:

* Fast inference
* Lightweight architecture

---

### Gemma3 1B

Strengths:

* Stable on 8GB RAM
* Good response quality
* Suitable for development

Selected as Development Model.

---

### TinyLlama

Strengths:

* Extremely lightweight
* Very fast inference

Used as a lightweight backup model.

---

## Final Model Decisions

### Development LLM

Gemma3 1B

Reason:

Runs reliably on available hardware while maintaining acceptable customer-support performance.

---

### Production LLM

Llama 3.1 8B

Reason:

Strong instruction following, high-quality responses, and excellent RAG compatibility.

---

### Embedding Model

nomic-embed-text

Reason:

Optimized for semantic search and retrieval tasks.

---

## Fine-Tuning vs RAG

For this project, RAG is preferred because customer-support information changes frequently.

Examples:

* Refund policies
* Shipping policies
* FAQs
* Account information

Fine-tuning may be added later for company-specific tone and response style.

---

## LoRA and QLoRA

### LoRA

Parameter-efficient fine-tuning using lightweight adapter layers.

### QLoRA

Combines quantization and LoRA to enable fine-tuning on consumer hardware.

---

## Potential Fine-Tuning Dataset

Example categories:

* Refund requests
* Delayed shipments
* Damaged products
* Order cancellations
* Password resets
* Subscription cancellations
* Account-related issues

---

# Current Architecture Plan

Customer Query

↓

Embedding Model (nomic-embed-text)

↓

ChromaDB Vector Store

↓

Retriever

↓

LLM (Gemma3 / Llama3.1)

↓

Final Response

---

# Current Status

## Day 1

Completed ✅

## Day 2

Completed ✅

---

# Next Phase

* Document Loading
* Text Chunking
* Embedding Generation
* ChromaDB Integration
* RAG Pipeline Development
* FastAPI Integration
* LangGraph Workflow Construction

---

## Author

Sangami Venu

B.Tech CSE

Agentic AI Learning Journey
