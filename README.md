## Problem Statement:

https://gist.github.com/vikas-t/724da4a118612a8a8faf0acd5e4e4567

##  Proposed Solution (Phase 1)

### 1. **Divide the data into Tiers**
- **Hot Tier** (Recent 3 months): Remain in Cosmos DB
- **Cold Tier** (Older than 3 months): Moved to Azure Blob Storage (Cool/Archive tier)

**Why?**
We maintain the Cosmos DB created for the hot storage as it is pre existing with API that needs to be maintained as per the solution requirements.
Shifting the older data to blob storage will help us reduce the cost for data that is not accessed frequently.

### 2. **Durable Azure Function to Archive older records**
- Move records older than 3 months from Cosmos DB to Blob Storage, after successful archiving delete from cosmos db.

**Why?**
We use Azure durable functions as it allows orchestrating a long-running, stateful process which is ideal for checking large datasets and ensuring "archive → verify → delete" is atomic.

We choose this over time-triggered functions as it does not manage retries/failure well and logic apps because logic apps offer limited control and observability in  comparison.

### 3. **Data Access Wrapper Layer**
- Implements a logic to check cosmos db first. If not found and record is old, fallback to Blob Storage

### 4. **CI/CD via Azure DevOps**
- Implementing pipelines to deploy Function and other components.

---

##  Tech Stack

- Azure Functions 
- Azure Cosmos DB
- Azure Blob Storage
- Python
- Azure DevOps
- VS Code

---

##  Folder Structure

├── billing_archiver/ 
├── billing_da/ 
├── pipelines/ 
├── diagrams/ # Architecture 
├── README.md
└── .gitignore


## Implementations to make system more robust and prod ready

- Enable CI/CD rollback or redeploy from last good build to avoid pipeline failures, also keep the infrastructure versioned(use IAC - bicep/ARM)
- Enable Application insights in all function apps
- To avoid unauthorized access, revoke public access, use security best practices, configure private endpoints for cosmos db and blob, set NSGs to specific subnet ranges and use managed identities and key vault for secrets
- We can implement CDN to cache recently accessed data from cold storage tier to reduce latency and split blob files if file size is too large
- To avoid archive function failure or timeout we can schedule it to run frequently with smaller batches but this might increase cost so we can create alert for function incase of failure, timeout, etc and we can restart instance manually if needed
- To avoid duplication we can make the functions idempotent. we can use logging per record ID to avoid duplication or loss and make sure to verify the archival of data before deletion
- to avoid our api becoming slow and failing to query cosmos db we can add auto scaling on cosmos Request Units and set retry policies and alerts when consumption is more than 80% 