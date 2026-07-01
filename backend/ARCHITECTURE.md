# SIDE Architecture Documentation

## System Architecture

```mermaid
graph TB
    subgraph "External Sources"
        Discord[Discord]
        Telegram[Telegram]
        Gmail[Gmail]
        GitHub[GitHub]
        Webhooks[Generic Webhooks]
    end
    
    subgraph "Webhook Layer"
        WH[Webhook Receiver]
        V[Signature Verification]
    end
    
    subgraph "Agent Layer"
        FC[Feedback Collector]
        FCL[Feedback Cleaner]
        CL[Classification]
        SE[Sentiment]
        SV[Severity]
        DD[Duplicate Detection]
        TG[Ticket Generation]
        PR[Priority]
        ME[Memory]
        IN[Insight]
        RD[Response Draft]
        SE2[Search]
        FE[Fetch]
        RO[Routing]
    end
    
    subgraph "LangGraph"
        FG[Feedback Graph]
        IG[Insight Graph]
    end
    
    subgraph "Memory Layer"
        Cognee[Cognee]
        KG[Knowledge Graph]
        VM[Vector Memory]
    end
    
    subgraph "Data Layer"
        Firestore[Firebase Firestore]
        Collections[14 Collections]
    end
    
    subgraph "Integration Layer"
        Groq[Groq LLM]
        Gemini[Gemini LLM]
        TinyFish[TinyFish API]
        SMTP[SMTP Email]
    end
    
    subgraph "API Layer"
        FastAPI[FastAPI]
        Routers[10 Routers]
        Middleware[Security/CORS/Rate Limit]
    end
    
    Discord --> WH
    Telegram --> WH
    Gmail --> WH
    GitHub --> WH
    Webhooks --> WH
    
    WH --> V
    V --> FC
    FC --> FG
    
    FG --> FCL
    FG --> CL
    FG --> SE
    FG --> SV
    FG --> SE2
    FG --> FE
    FG --> DD
    FG --> ME
    FG --> TG
    FG --> PR
    FG --> RD
    FG --> IN
    
    DD --> Cognee
    ME --> Cognee
    SE2 --> TinyFish
    FE --> TinyFish
    
    CL --> Groq
    CL --> Gemini
    SE --> Groq
    SE --> Gemini
    SV --> Groq
    SV --> Gemini
    
    TG --> Firestore
    PR --> Firestore
    ME --> Firestore
    
    IG --> IN
    IG --> Cognee
    
    FastAPI --> Routers
    Routers --> FG
    Routers --> IG
    
    RD --> SMTP
```

## Database Schema

### Collections

```mermaid
erDiagram
    users ||--o{ feedback : submits
    users ||--o{ tickets : creates
    users ||--o{ ticket_updates : writes
    users ||--o{ notifications : receives
    users ||--o{ activity_logs : generates
    
    organizations ||--o{ users : has
    organizations ||--o{ feedback : receives
    organizations ||--o{ tickets : owns
    organizations ||--o{ integrations : configures
    
    customers ||--o{ feedback : provides
    customers ||--o{ messages : sends
    
    feedback ||--o|| tickets : generates
    feedback ||--o|| duplicate_clusters : belongs_to
    feedback ||--o{ agent_runs : triggers
    
    tickets ||--o{ ticket_updates : has
    tickets ||--o{ duplicate_clusters : linked_to
    tickets ||--o{ agent_runs : triggers
    
    duplicate_clusters ||--o{ feedback : contains
    duplicate_clusters ||--o|| tickets : linked_to
    
    integrations ||--o{ organizations : belongs_to
```

### Firestore Collections

1. **users** - User accounts and profiles
2. **organizations** - Organization settings
3. **feedback** - Raw feedback from all sources
4. **tickets** - Generated tickets
5. **ticket_updates** - Ticket comments and updates
6. **duplicate_clusters** - Duplicate issue clusters
7. **customers** - Customer information
8. **messages** - Message history
9. **activity_logs** - User activity tracking
10. **notifications** - User notifications
11. **integrations** - Third-party integrations
12. **agent_runs** - Agent execution logs
13. **memory** - Long-term memory storage
14. **analytics** - Analytics metrics
15. **daily_reports** - Generated reports

## Agent Flow

```mermaid
sequenceDiagram
    participant User
    participant Webhook
    participant Collector
    participant Graph
    participant Agents
    participant Firestore
    participant Cognee
    participant LLM
    
    User->>Webhook: Send Feedback
    Webhook->>Collector: Process
    Collector->>Graph: Execute
    Graph->>Agents: Route to Agents
    
    Agents->>LLM: Classify
    LLM-->>Agents: Category
    
    Agents->>LLM: Sentiment
    LLM-->>Agents: Sentiment
    
    Agents->>LLM: Severity
    LLM-->>Agents: Severity
    
    Agents->>Cognee: Check Duplicates
    Cognee-->>Agents: Similar Items
    
    Agents->>LLM: Generate Ticket
    LLM-->>Agents: Ticket Data
    
    Agents->>Firestore: Store Ticket
    Agents->>Cognee: Store Memory
    
    Graph-->>User: Results
```

## LangGraph State Machine

```mermaid
stateDiagram-v2
    [*] --> Routing
    Routing --> Cleaning: clean
    Routing --> Classification: skip_cleaning
    Routing --> [*]: spam
    
    Cleaning --> Classification
    Classification --> Sentiment: analyze
    Classification --> Severity: skip
    
    Sentiment --> Severity
    Severity --> Search: search
    Severity --> DuplicateDetection: skip
    
    Search --> Fetch: fetch
    Search --> DuplicateDetection: skip
    Fetch --> DuplicateDetection
    
    DuplicateDetection --> TicketGeneration: generate
    DuplicateDetection --> MemoryStorage: skip
    
    TicketGeneration --> PriorityCalculation
    PriorityCalculation --> MemoryStorage
    
    MemoryStorage --> ResponseDraft: draft
    MemoryStorage --> [*]: skip
    
    ResponseDraft --> [*]
```

## Security Architecture

```mermaid
graph LR
    Client[Client] --> Middleware[Middleware Layer]
    Middleware --> Auth[JWT Auth]
    Auth --> Roles[Role Check]
    Roles --> RateLimit[Rate Limiting]
    RateLimit --> API[API Handler]
    
    API --> Repo[Repository Layer]
    Repo --> Firestore[Firebase Firestore]
    
    API --> Agent[Agent Layer]
    Agent --> LLM[LLM Provider]
    LLM --> Groq[Groq]
    LLM --> Gemini[Gemini]
```

## Background Processing

```mermaid
graph TB
    subgraph "Email Worker"
        Poll[Poll Gmail]
        Process[Process Email]
        Store[Store in DB]
        Poll --> Process
        Process --> Store
    end
    
    subgraph "Webhook Worker"
        Queue[Queue]
        ProcessW[Process Webhook]
        Retry[Retry Logic]
        Queue --> ProcessW
        ProcessW --> Retry
    end
    
    subgraph "Insight Worker"
        Schedule[Schedule]
        Generate[Generate Insights]
        StoreR[Store Reports]
        Schedule --> Generate
        Generate --> StoreR
    end
```

## LLM Provider Fallback

```mermaid
graph TD
    Request[Request][Request] --> Primary[Primary: Groq]
    Primary --> Success{Success?}
    Success --> Yes[Return Result]
    Success --> No[Fallback: Gemini]
    Fallback --> Success2{Success?}
    Success2 --> Yes2[Return Result]
    Success2 --> No2[Return Error]
```

## Memory Architecture

```mermaid
graph TB
    subgraph "Memory Input"
        Feedback[Feedback]
        Tickets[Tickets]
        Context[Context]
    end
    
    subgraph "Cognee"
        Vector[Vector DB]
        Graph[Knowledge Graph]
        Patterns[Pattern Detection]
    end
    
    subgraph "Memory Output"
        Similar[Similar Items]
        History[Historical Context]
        Trends[Recurring Patterns]
    end
    
    Feedback --> Vector
    Tickets --> Vector
    Context --> Graph
    
    Vector --> Similar
    Graph --> History
    Patterns --> Trends
```

## API Versioning

All APIs are versioned under `/api/v1/`:

```
/api/v1/auth/*
/api/v1/users/*
/api/v1/organizations/*
/api/v1/feedback/*
/api/v1/tickets/*
/api/v1/webhooks/*
/api/v1/agents/*
/api/v1/integrations/*
/api/v1/dashboard/*
```

## Error Handling

```mermaid
graph TD
    Error[Error Occurs] --> Type{Error Type?}
    Type --> Base[BaseException]
    Type --> HTTP[HTTPException]
    Type --> General[General Exception]
    
    Base --> Handler[Base Handler]
    HTTP --> Handler2[HTTP Handler]
    General --> Handler3[General Handler]
    
    Handler --> Log[Log Error]
    Handler2 --> Log
    Handler3 --> Log
    
    Log --> Response[JSON Response]
    Response --> Client[Client]
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production"
        LB[Load Balancer]
        App1[App Instance 1]
        App2[App Instance 2]
        App3[App Instance 3]
        
        LB --> App1
        LB --> App2
        LB --> App3
    end
    
    subgraph "External Services"
        Firebase[Firebase]
        Groq[Groq]
        Gemini[Gemini]
        Cognee[Cognee]
    end
    
    App1 --> Firebase
    App2 --> Firebase
    App3 --> Firebase
    
    App1 --> Groq
    App2 --> Groq
    App3 --> Groq
    
    App1 --> Gemini
    App2 --> Gemini
    App3 --> Gemini
    
    App1 --> Cognee
    App2 --> Cognee
    App3 --> Cognee
```
