## Project Flow

```mermaid
flowchart TD
    A[Start] --> B[Admin Login]
    B --> C{Valid Login?}
    C -->|No| B
    C -->|Yes| D[Dashboard]
    D --> E[Manage Menu]
    D --> F[Manage Customers]
    D --> G[Manage Orders]
    D --> H[View Sales Summary]
    E --> I[(PostgreSQL)]
    F --> I
    G --> I
    H --> I
    D --> J[Logout]
    J --> K[End]