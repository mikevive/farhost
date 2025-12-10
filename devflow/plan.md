# AI-Powered Development Environment - Comprehensive Plan

## Overview
Transform `/Users/mikevive/.farhost/dev` into a comprehensive AI-powered workspace leveraging Claude Code for L4→L5 career progression at GlossGenius.

---

## Table of Contents
1. [Directory Structure](#directory-structure)
2. [Workflow Details](#workflow-details)
   - [Active Development](#1-active-development)
   - [PR Workflows](#2-pr-workflows)
   - [Documentation](#3-documentation)
   - [Architecture](#4-architecture-l5-focus)
   - [Planning](#5-planning)
   - [Communication](#6-communication)
   - [Mentorship](#7-mentorship-l5-focus)
   - [Impact Tracking](#8-impact-tracking-l5-focus)
   - [Cross-Team](#9-cross-team-l5-focus)
3. [Integration with Git Worktrees](#integration-with-git-worktrees)
4. [Implementation Roadmap](#implementation-roadmap)
5. [Daily/Weekly Flow Examples](#usage-patterns)

---

## Directory Structure

```
/Users/mikevive/.farhost/dev/
├── README.md                           # Master documentation for the workspace
│
├── services/                           # Local development infrastructure
│   ├── postgres/                       # ✅ Already exists
│   │   ├── postgres.yaml
│   │   ├── init-scripts/
│   │   └── README.md
│   ├── redis/                          # Cache service (future)
│   ├── kafka/                          # Event streaming (future)
│   └── .claude/
│       ├── settings.json               # AI plugins for service management
│       └── commands/
│           ├── start-all-services.md
│           ├── stop-all-services.md
│           └── service-health-check.md
│
├── workflows/                          # AI-powered workflow automation
│   ├── active-development/            # L4/L5: Active coding workflows
│   │   ├── .claude/
│   │   │   ├── settings.json
│   │   │   └── commands/
│   │   │       ├── create-worktree.md          # Create new feature branch + Claude setup
│   │   │       ├── switch-context.md           # Switch between worktrees intelligently
│   │   │       ├── debug-session.md            # AI-assisted debugging workflow
│   │   │       ├── run-tests.md                # Test execution across worktrees
│   │   │       └── local-integration.md        # Multi-service local testing
│   │   ├── templates/
│   │   │   ├── feature-branch.template
│   │   │   ├── bugfix-branch.template
│   │   │   └── spike-branch.template
│   │   └── README.md
│   │
│   ├── pr-workflows/                   # L4/L5: Pull request management
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── create-pr.md                # AI-generated PR descriptions
│   │   │       ├── review-pr.md                # AI-assisted PR review
│   │   │       ├── pr-checklist.md             # Quality checklist generator
│   │   │       └── rebase-update.md            # Smart rebase handling
│   │   ├── templates/
│   │   │   ├── pr-description.template
│   │   │   ├── pr-review-comments.template
│   │   │   └── breaking-change-notice.template
│   │   └── README.md
│   │
│   ├── documentation/                  # L4/L5: Technical writing
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── create-adr.md               # Architecture Decision Record
│   │   │       ├── create-design-doc.md        # Technical design document
│   │   │       ├── create-prd.md               # Product Requirements Doc
│   │   │       ├── update-api-docs.md          # API documentation sync
│   │   │       └── create-runbook.md           # Operational runbooks
│   │   ├── templates/
│   │   │   ├── adr-template.md
│   │   │   ├── design-doc-template.md
│   │   │   ├── prd-template.md
│   │   │   ├── rfc-template.md
│   │   │   └── postmortem-template.md
│   │   ├── active/                             # In-progress docs
│   │   ├── published/                          # Completed docs
│   │   └── README.md
│   │
│   ├── architecture/                   # L5: System design & ownership
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── analyze-system.md           # System architecture analysis
│   │   │       ├── propose-refactor.md         # Refactoring proposals
│   │   │       ├── evaluate-tradeoffs.md       # Technical trade-off analysis
│   │   │       ├── create-tech-radar.md        # Technology radar updates
│   │   │       └── cross-service-impact.md     # Multi-service change analysis
│   │   ├── diagrams/                           # Architecture diagrams
│   │   ├── proposals/                          # Architecture proposals
│   │   ├── reviews/                            # Design review notes
│   │   └── README.md
│   │
│   ├── planning/                       # L4/L5: Project & sprint planning
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── break-down-epic.md          # Epic → stories breakdown
│   │   │       ├── estimate-effort.md          # Story point estimation
│   │   │       ├── create-sprint-plan.md       # Sprint planning assistant
│   │   │       ├── risk-analysis.md            # Risk identification
│   │   │       └── dependency-map.md           # Dependency mapping
│   │   ├── templates/
│   │   │   ├── epic-template.md
│   │   │   ├── user-story-template.md
│   │   │   └── sprint-goal-template.md
│   │   ├── active-sprints/
│   │   ├── backlog/
│   │   └── README.md
│   │
│   ├── communication/                  # L4/L5: Status updates & collaboration
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── generate-eod.md             # End-of-day update
│   │   │       ├── generate-eow.md             # End-of-week summary
│   │   │       ├── slack-response.md           # Draft Slack responses
│   │   │       ├── meeting-notes.md            # Meeting notes + action items
│   │   │       └── status-report.md            # Status report generation
│   │   ├── templates/
│   │   │   ├── eod-template.md
│   │   │   ├── eow-template.md
│   │   │   ├── 1-1-template.md
│   │   │   └── retrospective-template.md
│   │   ├── updates/                            # Historical updates
│   │   └── README.md
│   │
│   ├── mentorship/                     # L5: Knowledge sharing & coaching
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── create-learning-plan.md     # Personalized learning paths
│   │   │       ├── code-review-feedback.md     # Constructive feedback
│   │   │       ├── pair-programming-plan.md    # Pairing session prep
│   │   │       ├── interview-prep.md           # Technical interview questions
│   │   │       └── tech-talk-outline.md        # Tech talk preparation
│   │   ├── templates/
│   │   │   ├── mentorship-plan.template
│   │   │   ├── feedback-template.md
│   │   │   └── tech-talk-template.md
│   │   ├── mentees/                            # Per-mentee tracking
│   │   ├── resources/                          # Learning resources
│   │   └── README.md
│   │
│   ├── impact-tracking/                # L5: Metrics & measurable outcomes
│   │   ├── .claude/
│   │   │   └── commands/
│   │   │       ├── analyze-metrics.md          # Metrics analysis
│   │   │       ├── track-initiative.md         # Initiative progress tracking
│   │   │       ├── generate-impact-report.md   # Impact summary
│   │   │       ├── identify-improvements.md    # Improvement opportunities
│   │   │       └── team-health-check.md        # Team metrics analysis
│   │   ├── initiatives/                        # Active initiatives
│   │   ├── metrics/                            # Metric definitions
│   │   ├── reports/                            # Generated reports
│   │   └── README.md
│   │
│   └── cross-team/                     # L5: Multi-team initiatives
│       ├── .claude/
│       │   └── commands/
│       │       ├── alignment-doc.md            # Cross-team alignment
│       │       ├── api-contract.md             # Service contract definition
│       │       ├── migration-plan.md           # Multi-service migrations
│       │       └── stakeholder-update.md       # Stakeholder communication
│       ├── initiatives/
│       ├── contracts/
│       └── README.md
│
├── scripts/                            # Automation scripts
│   ├── create-worktree.sh             # Enhanced worktree creation
│   ├── setup-claude-config.sh         # Auto-setup Claude in worktrees
│   ├── sync-worktrees.sh              # Update all worktrees
│   ├── cleanup-old-worktrees.sh       # Remove merged branches
│   ├── service-manager.sh             # Start/stop services
│   ├── morning-routine.sh             # Morning startup automation
│   ├── eod-routine.sh                 # End-of-day automation
│   ├── backup-workspace.sh            # Workspace backup
│   └── README.md
│
├── templates/                          # Global templates
│   ├── .claude/
│   │   └── settings.json              # Base Claude configuration
│   ├── worktree-claude-config/
│   │   ├── kotlin-service/
│   │   ├── typescript-service/
│   │   ├── mobile-app/
│   │   └── infrastructure/
│   └── README.md
│
└── context/                           # Quick context switching
    ├── current-focus.md               # Current sprint/initiative focus
    ├── active-worktrees.md            # What's currently in progress
    ├── blockers.md                    # Current blockers
    └── weekly-goals.md                # Weekly objectives
```

---

## Workflow Details

### 1. Active Development

**Purpose:** Streamline day-to-day coding activities across multiple worktrees with AI assistance.

**Key Capabilities:**
- **Worktree Management**: Creates new feature branches with automatic Claude Code setup
- **Context Switching**: Intelligently switches between active worktrees
- **Local Testing**: Coordinates multi-service testing on your local machine
- **Debug Assistance**: AI-powered debugging sessions

**Example Usage:**

#### Starting a New Feature
```bash
cd ~/.farhost/dev/workflows/active-development
claude /create-worktree core-api add-payment-retries
```

**What Happens:**
1. Detects `core-api` is a Kotlin service
2. Creates worktree at `~/Documents/glossgenius/repos/core-api/add-payment-retries`
3. Copies Kotlin-specific Claude configuration (includes Gradle commands, DB migration helpers)
4. Checks Jira for matching ticket (e.g., "PAY-1234")
5. Links ticket context to the worktree
6. Shows recent related changes
7. Starts necessary services (postgres)

#### Switching Between Features
```bash
claude /switch-context
```

**Claude Shows:**
```
Active Worktrees:
1. core-api/add-payment-retries (PAY-1234) - 3 uncommitted files
2. core-ai-workflows/service-options (SOV-789) - Clean, PR in review
3. core-protos/payment-events - 1 commit ahead

Which worktree? [1-3]:
```

You select #2, Claude:
- Changes directory to that worktree
- Shows recent commits
- Checks PR status
- Verifies services are running

#### Local Integration Testing
```bash
claude /local-integration
```

**What Happens:**
- Detects active worktrees (`core-api`, `core-ai-workflows`)
- Verifies postgres is running
- Suggests test scenarios spanning both services
- Runs integration test suite
- Shows results with AI-analyzed failures

**Key Commands:**
- `/create-worktree <repo> <branch>` - Create and setup new worktree
- `/switch-context [name]` - Switch between worktrees intelligently
- `/debug-session` - Start AI-assisted debugging
- `/run-tests [scope]` - Run tests with smart filtering
- `/local-integration` - Multi-service testing coordination

---

### 2. PR Workflows

**Purpose:** Accelerate PR creation and reviews with AI-generated content and analysis.

**Key Capabilities:**
- **Smart PR Creation**: Analyzes changes and generates comprehensive PR descriptions
- **Code Review Assistance**: Reviews PRs with security, performance, and best practice checks
- **Quality Checklists**: Context-aware checklists based on what changed
- **Rebase Help**: Assists with complex rebases and conflict resolution

**Example Usage:**

#### Creating a PR
```bash
cd ~/.farhost/dev/workflows/pr-workflows
claude /create-pr
```

**What Claude Does:**
1. Analyzes all commits in your branch vs main
2. Reads changed files to understand implementation
3. Checks Jira ticket for context
4. Looks at recent PRs to match style
5. Generates comprehensive description
6. Suggests reviewers
7. Creates PR with proper labels

**Generated PR Description:**
```markdown
Title: feat(payments): Add exponential backoff retry mechanism for webhooks

## Summary
Implements a robust retry mechanism for failed payment webhooks with:
- Exponential backoff strategy (1s, 2s, 4s, 8s, 16s)
- Maximum 5 retry attempts
- Dead letter queue for permanently failed webhooks
- Observability with metrics and structured logging

## Technical Changes
- New `WebhookRetryService` with configurable backoff policy
- Database migration adds `retry_count` and `next_retry_at` columns
- Integration with existing `PaymentWebhookProcessor`
- Circuit breaker to prevent cascading failures

## Testing
- [x] Unit tests for retry logic (WebhookRetryServiceTest.kt)
- [x] Integration tests with test containers
- [x] Load tested with 10K webhooks/minute
- [x] Verified metrics in local Grafana

## Rollout Plan
- Feature flag: `payment_webhook_retries_enabled`
- Gradual rollout: 1% → 10% → 50% → 100% over 1 week
- Monitoring: webhook_retry_success_rate, webhook_retry_exhausted_count

## Related
- Jira: PAY-1234
- Design Doc: [link]
- Closes #456

🤖 Generated with Claude Code
```

#### Reviewing a PR
```bash
claude /review-pr https://github.com/GlossGenius/core-api/pull/789
```

**What Claude Analyzes:**
- **Security**: SQL injection, XSS, auth bypasses, secrets in code
- **Performance**: N+1 queries, inefficient algorithms, memory leaks
- **Best Practices**: Error handling, logging, code organization
- **Testing**: Test coverage, edge cases
- **Documentation**: Missing docs, unclear variable names

**Generated Review:**
```markdown
## Overall Assessment
Strong implementation with good test coverage. A few suggestions below.

## 🔴 Critical Issues
None found

## 🟡 Suggestions

### 1. Potential N+1 Query (PaymentService.kt:145)
[Code example and fix]

### 2. Error Handling (WebhookController.kt:67)
[Suggestion with explanation]

### 3. Test Coverage
[Missing test cases]

## ✅ Strengths
- Excellent use of sealed classes
- Comprehensive logging
- Good separation of concerns

## Questions
1. Database migration impact during active processing?
2. Maximum age for retries?
```

#### Pre-Review Checklist
```bash
claude /pr-checklist
```

**Context-Aware Checklist:**
- Detects database migrations → adds migration-specific checks
- Detects query changes → adds performance checks
- Detects auth changes → adds security checks
- Detects API changes → adds documentation checks

**Key Commands:**
- `/create-pr` - Generate PR with comprehensive description
- `/review-pr <url>` - AI-powered code review
- `/pr-checklist` - Context-aware quality checklist
- `/rebase-update` - Guided rebase assistance
- `/pr-summary <url>` - Quick summary of external PR

---

### 3. Documentation

**Purpose:** Create high-quality technical documentation quickly with AI assistance and templates.

**Key Capabilities:**
- **ADRs**: Document important technical decisions
- **Design Docs**: Comprehensive technical designs for major features
- **PRDs**: Product Requirements Documents
- **Runbooks**: Operational documentation
- **API Docs**: Keep API documentation in sync with code

**Example Usage:**

#### Writing an ADR
```bash
cd ~/.farhost/dev/workflows/documentation
claude /create-adr "Use exponential backoff for webhook retries"
```

**What Claude Does:**
1. Asks clarifying questions (problem, alternatives, consequences)
2. Generates structured ADR with:
   - Status, Context, Decision
   - Alternatives Considered with pros/cons
   - Consequences (positive, negative, risks)
   - Implementation Notes

**Generated ADR Structure:**
```markdown
# ADR 042: Use Exponential Backoff for Webhook Retries

## Status
Proposed

## Context
[Problem statement, requirements]

## Decision
[Chosen approach with parameters]

## Alternatives Considered
### 1. Fixed Interval Retry
**Pros:** Simple
**Cons:** Doesn't respect rate limits

### 2. Linear Backoff
**Pros:** Gradual increase
**Cons:** Too slow for transient failures

## Consequences
### Positive
- Automatic recovery from transient failures
- Respects rate limits

### Negative
- Delayed processing
- Database storage needed

### Risks
- Must ensure idempotency
- Clock skew handling

## Implementation Notes
[Technical details]

## Related
[Links to design docs, Jira, similar patterns]
```

#### Creating a Design Doc
```bash
claude /create-design-doc
```

**Claude Prompts For:**
- Feature name
- Problem statement
- Constraints

**Generated Design Doc Sections:**
1. Overview & Problem Statement
2. Goals & Non-Goals
3. Proposed Solution with architecture diagrams
4. Data Model with examples
5. API Design with request/response examples
6. Technical Considerations (performance, security, scalability)
7. Migration Strategy with phases
8. Testing Plan
9. Rollback Plan
10. Metrics
11. Open Questions
12. Alternatives Considered

#### Creating a PRD
```bash
claude /create-prd
```

**Claude Walks Through:**
- User stories
- Success metrics
- Technical feasibility
- Dependencies
- Timeline

**Key Commands:**
- `/create-adr <topic>` - Architecture Decision Record
- `/create-design-doc` - Comprehensive technical design
- `/create-prd` - Product Requirements Document
- `/create-runbook <service>` - Operational runbook
- `/update-api-docs` - Sync code changes to API docs

---

### 4. Architecture (L5 Focus)

**Purpose:** Lead large-scale architectural initiatives and system ownership.

**Key Capabilities:**
- **System Analysis**: Deep-dive into service architecture and dependencies
- **Refactoring Proposals**: Identify and propose technical improvements
- **Cross-Service Impact Analysis**: Understand ripple effects of changes
- **Tech Radar**: Track technology adoption across the organization

**Example Usage:**

#### Analyzing a System for Ownership
```bash
cd ~/.farhost/dev/workflows/architecture
claude /analyze-system core-api/payments
```

**What Claude Does:**
1. Scans the payments module
2. Identifies dependencies (upstream and downstream)
3. Analyzes patterns and architectural style
4. Identifies technical debt and improvement opportunities

**Generated Report Sections:**
- Architecture overview with diagrams
- Dependencies (who calls us, who we call)
- Code quality assessment (strengths, technical debt)
- Performance characteristics
- Improvement opportunities ranked by impact
- Recommended next steps with timeline

#### Proposing a Major Refactor
```bash
claude /propose-refactor "Split PaymentService into domain-specific services"
```

**Claude Generates:**
- Current state analysis
- Proposed new structure
- Migration path
- Trade-offs (complexity vs maintainability)
- Rollout strategy
- Rollback plan

#### Evaluating Cross-Service Impact
```bash
claude /cross-service-impact "Migrate payments API from gRPC to REST"
```

**What Claude Does:**
1. Searches all repos for gRPC calls to payments service
2. Identifies calling services
3. Analyzes proto definitions
4. Estimates migration effort per service

**Generated Analysis:**
- Affected services with impact level
- Usage patterns per service
- Migration effort estimates
- Recommended migration strategy (parallel run vs big bang)
- Phase-by-phase plan
- Risks and mitigation
- Success metrics

**Key Commands:**
- `/analyze-system <service>` - Deep architectural analysis
- `/propose-refactor <description>` - Refactoring proposal with trade-offs
- `/cross-service-impact <change>` - Ripple effect analysis
- `/create-tech-radar` - Technology adoption recommendations
- `/evaluate-tradeoffs <decision>` - Technical trade-off analysis

---

### 5. Planning

**Purpose:** Break down large projects and estimate effort with AI assistance.

**Key Capabilities:**
- **Epic Breakdown**: Converts epics into actionable user stories
- **Effort Estimation**: Helps estimate story points based on complexity
- **Sprint Planning**: Assists with sprint planning and capacity allocation
- **Dependency Mapping**: Identifies dependencies between tasks
- **Risk Analysis**: Flags technical and timeline risks

**Example Usage:**

#### Breaking Down an Epic
```bash
cd ~/.farhost/dev/workflows/planning
claude /break-down-epic PAY-5678
```

**What Claude Does:**
1. Fetches epic from Jira
2. Reads description and acceptance criteria
3. Analyzes technical complexity
4. Generates user stories with:
   - User story format
   - Acceptance criteria
   - Technical notes
   - Dependencies
   - Estimates
   - Risk level

**Generated Output:**
- 8-12 user stories with full details
- Dependency graph visualization
- Summary (total points, duration, risks)
- Option to create Jira tickets automatically

#### Sprint Planning
```bash
claude /create-sprint-plan
```

**Claude Asks:**
- Sprint duration
- Team capacity
- Current priorities

**Claude Generates:**
- Sprint goal
- Committed stories with assignments
- Week-by-week schedule
- Risk identification
- Success criteria

**Key Commands:**
- `/break-down-epic <epic-id>` - Convert epic to user stories
- `/estimate-effort <story>` - Help estimate story points
- `/create-sprint-plan` - Generate sprint plan based on capacity
- `/dependency-map` - Visualize task dependencies
- `/risk-analysis <initiative>` - Identify technical and timeline risks

---

### 6. Communication

**Purpose:** Automate routine communication tasks with AI-generated updates.

**Key Capabilities:**
- **EOD Updates**: Daily progress summaries from git activity
- **EOW Summaries**: Weekly accomplishments and next week planning
- **Slack Responses**: Draft thoughtful responses to technical questions
- **Meeting Notes**: Structure notes and extract action items
- **Status Reports**: Generate stakeholder updates

**Example Usage:**

#### End of Day Update
```bash
cd ~/.farhost/dev/workflows/communication
claude /generate-eod
```

**What Claude Does:**
1. Analyzes today's git commits across all worktrees
2. Checks Jira for ticket updates
3. Reviews PR activity (created, reviewed, merged)
4. Checks calendar for meetings (if integrated)

**Generated Update:**
```markdown
## EOD Update - Dec 9, 2025

### ✅ Completed
- **PAY-1234:** Completed webhook retry implementation
  - Added WebhookRetryService
  - Database migration
  - 95% test coverage
  - PR created: #456

- **Code Review:** Reviewed PR #789
  - Provided feedback on N+1 query
  - Approved after changes

### 🔄 In Progress
- **PAY-1234:** Addressing PR feedback
  - Need integration tests
  - ETA: Tomorrow morning

### 🚧 Blockers
- None

### 📅 Tomorrow
- Complete integration tests
- Start async webhook processing design doc
- 1:1 with Alice at 2pm

### 📊 Metrics
- Commits: 8
- PRs created: 1
- PRs reviewed: 1
- Tests added: 15

---
*Generated by Claude Code*
```

#### Weekly Summary
```bash
claude /generate-eow
```

**Generated Summary:**
- Key accomplishments (3-5 major items)
- Impact metrics (code, PRs, documentation, meetings)
- Learning & growth (L5 progress indicators)
- Next week priorities
- Risks & blockers
- Shout outs

#### Drafting Slack Response
```bash
claude /slack-response "Question about webhook retry behavior"
```

**Claude Prompts:**
- Paste the question/context
- What do they need to know?
- Technical level of audience

**Claude Generates:**
- Clear explanation with appropriate technical depth
- Current state vs new behavior
- Timeline and rollout plan
- Immediate fix if needed
- Links to relevant docs/PRs

**Key Commands:**
- `/generate-eod` - Daily update from git activity
- `/generate-eow` - Weekly summary with accomplishments
- `/slack-response <context>` - Draft Slack responses
- `/meeting-notes` - Structure meeting notes
- `/status-report <audience>` - Stakeholder-appropriate updates

---

### 7. Mentorship (L5 Focus)

**Purpose:** Scale your impact through formal mentorship and knowledge sharing.

**Key Capabilities:**
- **Learning Plans**: Create personalized learning paths for mentees
- **Code Review Feedback**: Generate constructive, educational feedback
- **Pairing Sessions**: Plan and prepare for pair programming
- **Interview Prep**: Create interview questions and evaluation criteria
- **Tech Talks**: Outline presentations and workshops

**Example Usage:**

#### Creating a Learning Plan
```bash
cd ~/.farhost/dev/workflows/mentorship
claude /create-learning-plan "Junior Engineer - Sarah" "System Design"
```

**Generated Learning Plan:**
- Current state assessment
- Learning goals (specific, measurable)
- 3-month phased plan:
  - Phase 1: Foundations (readings, exercises, analysis)
  - Phase 2: Hands-on practice (projects, pairing)
  - Phase 3: Independent application (lead feature, teach others)
- Assessment criteria per phase
- Resources (books, internal docs, practice platforms)
- Mentor notes

#### Code Review Feedback (Educational)
```bash
claude /code-review-feedback https://github.com/GlossGenius/core-api/pull/892
```

**Generated Educational Review:**
1. **Overall Assessment**: Positive framing
2. **Learning Opportunities**: 3-5 suggestions with:
   - Current code
   - Suggested improvement
   - Explanation of "why"
   - Further reading links
   - Examples from codebase
3. **What I Loved**: Positive reinforcement
4. **Questions for Mentee**: Thought-provoking questions
5. **Next Steps**: Pairing offers, related resources

**Tone**: Encouraging, educational, specific, actionable

#### Preparing a Tech Talk
```bash
claude /tech-talk-outline "Webhook Patterns: Retry, Idempotency, and Security"
```

**Generated Outline:**
- Talk structure with timing (intro, 4-5 main sections, Q&A)
- Each section includes:
  - Hook or key insight
  - Code examples (before/after)
  - Live demo ideas
  - Diagrams
- Supporting materials (slides, demo checklist)
- Anticipated questions with answers
- Resources to share
- Prep checklist

**Key Commands:**
- `/create-learning-plan <mentee> <focus>` - Personalized learning path
- `/code-review-feedback <pr-url>` - Educational code review
- `/pair-programming-plan <topic>` - Prepare for pairing session
- `/interview-prep <level>` - Interview questions and rubric
- `/tech-talk-outline <topic>` - Presentation structure and content

---

### 8. Impact Tracking (L5 Focus)

**Purpose:** Track and demonstrate measurable impact of your initiatives.

**Key Capabilities:**
- **Metrics Analysis**: Connect to monitoring systems and analyze trends
- **Initiative Tracking**: Track progress of major projects with milestones
- **Impact Reports**: Generate executive summaries of impact
- **Improvement Identification**: Analyze data to find optimization opportunities
- **Team Health**: Track team metrics (velocity, quality, morale)

**Example Usage:**

#### Tracking an Initiative
```bash
cd ~/.farhost/dev/workflows/impact-tracking
claude /track-initiative "Webhook Retry Mechanism"
```

**What Claude Does:**
1. Asks for baseline metrics
2. Sets up tracking for key metrics
3. Creates milestone tracking
4. Schedules check-ins

**Generated Tracking Document:**
- Overview (ID, owner, dates, status)
- Problem statement
- Success metrics table (baseline, target, current)
- Business impact (quantitative and qualitative)
- Timeline & milestones with deliverables
- Lessons learned
- Next steps

#### Generating Impact Report
```bash
claude /generate-impact-report "Q4 2025"
```

**Generated Report Sections:**
1. **Executive Summary**: High-level overview
2. **Major Initiatives**: 3-5 initiatives with impact details
3. **Code Contributions**: Volume and quality metrics
4. **Technical Leadership**: Design docs, ADRs, tech talks, reviews
5. **Collaboration & Mentorship**: Mentees, knowledge sharing, cross-team work
6. **Outcome Ownership**: Results driven, projects delivered
7. **Growth & Development**: L4→L5 progression indicators
8. **Metrics Summary**: Table of key numbers
9. **Next Quarter Goals**: Forward-looking objectives

**Key Commands:**
- `/track-initiative <name>` - Track major initiative with milestones
- `/analyze-metrics <initiative>` - Analyze metrics and trends
- `/generate-impact-report <period>` - Executive summary of impact
- `/identify-improvements` - Find optimization opportunities
- `/team-health-check` - Team metrics analysis

---

### 9. Cross-Team (L5 Focus)

**Purpose:** Lead initiatives that span multiple teams and require organizational alignment.

**Key Capabilities:**
- **Alignment Documents**: Create documents that align teams on shared goals
- **API Contracts**: Define service contracts and SLAs
- **Migration Plans**: Coordinate complex multi-service migrations
- **Stakeholder Updates**: Communicate with non-technical stakeholders
- **Dependency Management**: Track cross-team dependencies

**Example Usage:**

#### Creating Alignment Document
```bash
cd ~/.farhost/dev/workflows/cross-team
claude /alignment-doc "API Standardization Initiative"
```

**Generated Alignment Document:**
1. **Executive Summary**: One-paragraph overview
2. **Problem Statement**: Current state, impact of problem
3. **Proposed Solution**: Target state, rationale
4. **Teams & Stakeholders**: Core teams, supporting teams, stakeholders with roles
5. **Success Criteria**: Must-have, nice-to-have, metrics
6. **Timeline**: Phase-by-phase plan with owners
7. **Communication Plan**: Meetings, Slack, updates, demos
8. **Risks & Mitigation**: Top 4-5 risks with mitigation strategies
9. **Decision Log**: Key decisions with rationale
10. **Resources**: Documentation, tools, support contacts
11. **Success Stories**: Celebration milestones

**Key Commands:**
- `/alignment-doc <initiative>` - Cross-team alignment document
- `/api-contract <service>` - Service contract with SLA
- `/migration-plan <change>` - Multi-service migration coordination
- `/stakeholder-update <initiative>` - Non-technical status update
- `/dependency-map <project>` - Visualize cross-team dependencies

---

## Integration with Git Worktrees

### Enhanced Worktree Creation

**Script: `/dev/scripts/create-worktree.sh`**
- Determines service type (Kotlin/TypeScript/Mobile/Infra)
- Applies appropriate Claude configuration
- Auto-links Jira ticket if branch follows convention
- Sets up environment variables
- Initializes Claude with GlossGenius plugins

### Worktree-Aware Commands

All workflow commands understand worktrees:
- `/switch-context` lists all active worktrees with status
- `/local-integration` detects checked out worktrees, starts relevant services
- `/create-pr` knows which worktree you're in, fetches correct context

### Worktree Registry

**File: `/dev/context/active-worktrees.md`** (auto-updated)

Tracks:
- Active worktrees per repository
- Jira ticket links
- Status (in progress, in review)
- PR links

**Example:**
```markdown
# Active Worktrees

## core-api
- **integration**: Main integration testing branch
- **add-payment-webhooks**: PAY-1234 - Webhook retry mechanism
  - Status: In progress
  - PR: #456 (In review)

## core-ai-workflows
- **service-options**: SOV-789 - Service option pricing
- **create-appointment**: APT-456 - Appointment creation flow
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Goal:** Basic structure and priority workflows

**Tasks:**
1. Create directory structure
2. Setup services/ with existing postgres + future service templates
3. Create base Claude configuration templates
4. Implement enhanced worktree creation script

**Deliverables:**
- [ ] Full directory structure created
- [ ] Base templates in place
- [ ] Worktree script functional

---

### Phase 2: Active Development & PR Workflows (Week 2)
**Goal:** Core daily workflows operational

**Tasks:**
1. Implement active-development workflow
   - create-worktree command
   - switch-context command
   - local-integration command
2. Create PR workflow commands
   - create-pr command
   - review-pr command
   - pr-checklist command
3. Test with 2-3 active worktrees

**Deliverables:**
- [ ] Can create worktrees with Claude setup in <30 seconds
- [ ] Can switch contexts intelligently
- [ ] Can create PRs with AI-generated descriptions
- [ ] Can review PRs with AI assistance

---

### Phase 3: Documentation & Communication (Week 3)
**Goal:** Enable documentation and status updates

**Tasks:**
1. Setup documentation workflow
   - create-adr command
   - create-design-doc command
   - create-prd command
2. Setup communication workflow
   - generate-eod command
   - generate-eow command
   - slack-response command
3. Create templates for all document types

**Deliverables:**
- [ ] Can create ADRs, design docs, PRDs with AI assistance
- [ ] Can generate EOD/EOW updates automatically
- [ ] Can draft Slack responses

---

### Phase 4: L5 Workflows (Week 4)
**Goal:** All L5 capabilities in place

**Tasks:**
1. Implement architecture workflow
   - analyze-system command
   - propose-refactor command
   - cross-service-impact command
2. Setup planning workflow
   - break-down-epic command
   - create-sprint-plan command
3. Implement mentorship workflow
   - create-learning-plan command
   - code-review-feedback command
   - tech-talk-outline command
4. Setup impact tracking workflow
   - track-initiative command
   - generate-impact-report command
5. Implement cross-team workflow
   - alignment-doc command
   - migration-plan command

**Deliverables:**
- [ ] All L5 workflow directories functional
- [ ] Can track initiatives and generate impact reports
- [ ] Can create learning plans and educational reviews
- [ ] Can create cross-team alignment documents

---

### Phase 5: Automation & Polish (Week 5)
**Goal:** Automation and refined experience

**Tasks:**
1. Create morning routine script
2. Create EOD routine script
3. Implement proactive health checks
4. Setup weekly automation (cleanup, reports)
5. Create comprehensive README
6. Document all workflows

**Deliverables:**
- [ ] Morning/EOD routines functional
- [ ] Automated cleanup working
- [ ] All workflows documented
- [ ] Master README complete

---

## Usage Patterns

### Daily Flow Example

**Morning:**
```bash
cd ~/.farhost/dev
./scripts/morning-routine.sh
# → Starts services
# → Shows active worktrees
# → Displays today's goals from context/weekly-goals.md
```

**Active Development:**
```bash
cd workflows/active-development
claude /switch-context payment-webhooks
# Work on feature...

# When done:
cd workflows/pr-workflows
claude /create-pr
```

**End of Day:**
```bash
cd workflows/communication
claude /generate-eod
# Copy output to Slack

./scripts/eod-routine.sh
# → Commits any docs
# → Updates blockers
# → Shuts down services
```

---

### Weekly Flow Example

**Monday:**
- Sprint planning (`/workflows/planning`)
- Update weekly goals (`context/weekly-goals.md`)

**Tuesday-Thursday:**
- Active development (`/workflows/active-development`)
- PR reviews (`/workflows/pr-workflows`)
- Documentation as needed (`/workflows/documentation`)

**Friday:**
- Generate EOW update (`/workflows/communication`)
- Check initiative progress (`/workflows/impact-tracking`)
- Prep next week (mentorship 1:1s, tech talk prep)
- Run weekly cleanup script

---

### L5 Progression Flow

**L4 Work (Daily):**
- `active-development` - Coding
- `pr-workflows` - Reviews
- `documentation` - Design docs

**L5 Work (Weekly):**
- `architecture` - System proposals
- `mentorship` - 1:1s, code review coaching
- `communication` - Stakeholder updates

**L5 Work (Monthly):**
- `impact-tracking` - Initiative reviews
- `cross-team` - Alignment meetings
- `planning` - Roadmap contributions

---

## Key Benefits

### For L4 Activities
- ⚡ **Faster Development**: Worktree + Claude setup in <30 seconds
- 📝 **Better PRs**: AI-generated descriptions with proper context (2 min vs 15 min)
- 📚 **Comprehensive Documentation**: Templates + AI assistance for ADRs/design docs (30 min vs 3 hours)
- 📊 **Efficient Planning**: AI-assisted epic breakdown and estimation
- 💬 **Consistent Communication**: Automated EOD/EOW updates (1 min vs 10 min)

### For L5 Activities
- 📈 **Strategic Impact**: Track initiatives with measurable outcomes
- 🤝 **Cross-Team Influence**: Alignment docs + migration planning tools
- 🏗️ **System Ownership**: Deep analysis + refactoring proposals
- 👥 **Mentorship Scale**: Structured feedback + learning plans
- 🔍 **Problem Finding**: AI-assisted opportunity identification

### Productivity Multipliers
- Context Switching: <30 seconds between worktrees
- PR Creation: 2 minutes instead of 15
- Design Docs: 30 minutes instead of 3 hours
- EOD Updates: 1 minute instead of 10
- Initiative Tracking: Automated instead of manual spreadsheets

---

## Next Steps

1. **Review Plan**: Confirm this structure meets your needs
2. **Begin Implementation**: Start with Phase 1 (foundation)
3. **Iterate**: Build incrementally, validate with real usage
4. **Refine**: Update patterns and templates based on experience
5. **Scale**: Expand to additional workflows as needed

---

**Document Version:** 1.0
**Created:** Dec 9, 2025
**Status:** Ready for Implementation
