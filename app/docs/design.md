# Design Document

## Services

### Integration Service

**Responsibility:** Acts as an adapter or interface to multiple chat platforms.
**Implementation:** Written in Rust to minimize resource usage on limited hardware.
**Deployment:** Runs on the Raspberry Pi
**Resource Usage:** Primarily network-bound.

### Web Backend Service

**Responsibility:** Orchestrates the translation process and implements all high-level business logic.
**Implementation:** Written in Rust for efficiency on constrained hardware.
**Deployment:** Runs on the Raspberry Pi
**Resource Usage:** Network and CPU usage, with minor disk I/O for message caching.

### AI Inference Service

**Responsibility:** Runs the AI translation model inference.
**Implementation:** Developed in Python using FastAPI and CTranslate2.
**Model:** Two MarianMT Big models (English → Hungarian and Hungarian → English).
**Deployment:** Runs on the Orange Pi 3B to leverage its stronger CPU and memory resources.
**Resource Usage:** Heavy compute requirements, particularly CPU and RAM.

---

## Service Characteristics

* **Integration Service:** Primarily network usage
* **Web Backend Service:** Network and CPU usage, with some disk I/O
* **AI Inference Service:** High CPU and RAM consumption

---

## Hardware Environment

* **Raspberry Pi 2B+:**

  * 1 core, 700 MHz ARMv6 32-bit CPU
  * 512 MB RAM
  * Runs the Integration Service and Web Backend Service
  * Serves as the Docker Swarm master
  * Limited performance, suitable only for lightweight services

* **Orange Pi 3B:**

  * 4 cores, 1.8 GHz ARMv8.2-A 64-bit CPU
  * 4 GB RAM
  * Runs the AI Inference Service
  * Well-suited for compute-intensive workloads such as translation models
