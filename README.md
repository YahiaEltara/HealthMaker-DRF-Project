# HealthMaker-DRF-Project



- **Relationships**:
  - Each `client` must have **1 coach**.
  - Each `coach` can have **1 or more clients** (or none).
  - Each `client` can have **1 workout plan** (or none).
  - Each `workout plan` can have **1 or more meals**, where each meal must be unique per workout plan (or none).
  - Each `client` cannot have **two meals** with the same type.
  - Each `coach` can create **1 or more workout plans** (or none).
  - Each `coach` can create **1 or more meals** (or none).
  - Each `client` can have **1 or more recommendations** (or none).
  - Each `coach` can write **1 or more recommendations per client** (or none).
  - Each `recommendation` must have **1 client** and **1 coach**.
