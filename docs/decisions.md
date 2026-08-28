# Architectural Decisions

### DECISION-01: Product Concept - Arceus
- **Decision:** Build an automated mock data generator over forking the TrueForge repo.
- **Alternatives Considered:** Building an incident responder, building a multi-agent research desk, forking TrueForge.
- **Why:** Given the 48-hour timeline, Arceus is the most scoped-down idea that perfectly hits the required judging criteria (MCP, Sandbox, Human Approval). Forking TrueForge would violate the "Use of sponsor tools" judging criteria.
- **Trade-off Accepted:** We lose some of the "flashiness" of a complex multi-agent system, trading it for a guaranteed, finished MVP.
- **Confidence:** High.
- **Reversibility:** Low (Time constraint means we must commit to this path).