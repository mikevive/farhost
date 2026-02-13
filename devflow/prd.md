# Product Requirements Document: DevFlow

## 1. Project Overview
**Project Name:** DevFlow
**Goal:** A local-first, keyboard-centric Terminal User Interface (TUI) for high-performance time tracking and flow analysis.
**Platform:** Cross-platform (Windows/macOS/Linux via Python).
**Database Location:** `~/.farhost/devflow/devflow.db`

## 2. Core Functional Requirements

### A. Data Hierarchy
- **Categories (Transversal):** Labels describing the *nature* of work (e.g., `Code`, `Document`, `Distraction`, `Meeting`).
- **Projects:** The specific *stream* or client (e.g., `App-Redesign`, `Personal-Site`).
- **Tasks:** Granular *actions* belonging to a Project (e.g., `API Integration`).

### B. The Live Timer
- **Selection:**
  - User selects a Project first, which filters the available Tasks
  - Within filtered Tasks, user can further search/filter by typing
  - Finally, user selects a Category label
- **Starting a Timer:**
  - If a timer is already running, automatically stop and save the previous timer
  - Start the new timer immediately with the selected Project/Task/Category
- **Persistence:** Save `start_time` to an `active_session` table
- **Display:** Reactive HH:MM:SS clock showing elapsed time
- **Stopping a Timer:**
  - Immediately save the entry to `time_entries` table
  - Display the saved entry with an option to edit it (adjust times, change category/task)
  - No minimum duration - track entries down to the second
- **Midnight Handling:**
  - If a timer runs past midnight (00:00:00), automatically split it into two entries:
    - Entry 1: Ends at 23:59:59 on the start date
    - Entry 2: Starts at 00:00:00 on the next date
  - This ensures accurate daily reporting

### C. Data Management
- **Interface:** Dedicated setup/management screen accessible via vim-style command (e.g., `:manage` or `:setup`)
- **Operations:** Full CRUD (Create, Read, Update, Delete) for:
  - Categories
  - Projects
  - Tasks (linked to Projects)
- **Editing Time Entries:**
  - Users can edit any past time entry (modify start/end times, change category/task/project)
  - Users can delete any time entry
  - Allow overlapping entries without validation (user freedom)

### D. Daily Reporting
- **Goal:** Real-time visibility into the current day's productivity
- **Daily Log:** A chronological list of all completed time entries for the current date
- **Daily Totals:** Sum of hours grouped by Project and Category for "Today" (00:00:00 to 23:59:59)
- **Access:** Available via vim-style command (e.g., `:daily`)

### E. Weekly Dynamic Reporting
- **Logic:** Reports follow the ISO week (Monday to Sunday)
- **Current Week:** Automatically aggregates data from the most recent Monday through the current time
- **Historical Navigation:** Users can navigate to past weeks using keyboard shortcuts
- **Visualization:**
  - ASCII horizontal bar charts (using block characters) showing hours per day
  - Day-by-day display (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
  - Total hours per Category/Project
- **Access:** Available via vim-style command (e.g., `:weekly`)

## 3. User Interface & Navigation

### A. Navigation Philosophy
- **Vim-style command mode:** Press `:` to enter command mode, type commands to navigate
- **Example commands:**
  - `:timer` or `:t` - Go to timer view
  - `:daily` or `:d` - Show daily report
  - `:weekly` or `:w` - Show weekly report
  - `:manage` or `:m` - Open data management screen
  - `:quit` or `:q` - Exit application

### B. Keyboard Shortcuts
- **Philosophy:** Vim-inspired keybindings throughout the application
- **Navigation:** `hjkl` for movement (left, down, up, right)
- **Actions:** Standard vim conventions where applicable
- **Cancel/Back:** `Esc` key
- **Quit:** `:q` command

### C. Startup Behavior
- **Default View:** Timer view (main screen)
- **Database Check:** Verify database exists at `~/.farhost/devflow/devflow.db`, create if missing
- **Active Session Check:** Check for active timer in `active_session` table

### D. Crash Recovery
- **Behavior:** If app crashes while a timer is running:
  - On restart, detect the orphaned active session
  - Automatically stop the timer at the crash time (based on last known state)
  - Save the entry to `time_entries`
  - Clear the `active_session` table
  - No user prompt needed - handle automatically

## 4. Data Architecture (SQLite)

**Database Location:** `~/.farhost/devflow/devflow.db`

| Table | Columns | Purpose |
| :--- | :--- | :--- |
| `categories` | `id` (PK), `name` | Transversal labels (Code, Meeting, etc.) |
| `projects` | `id` (PK), `name` | Work streams or clients |
| `tasks` | `id` (PK), `project_id` (FK), `name` | Granular actions within a project |
| `time_entries` | `id` (PK), `task_id` (FK), `category_id` (FK), `start` (TIMESTAMP), `end` (TIMESTAMP), `duration_seconds` (INT) | Completed time tracking entries |
| `active_session` | `id` (PK), `task_id` (FK), `category_id` (FK), `start_time` (TIMESTAMP) | Currently running timer (0 or 1 row) |

**Notes:**
- Use local system timezone for all timestamps
- `time_entries.duration_seconds` is calculated as `end - start`
- `active_session` should only ever contain 0 or 1 row (enforced in application logic)
- When starting a new timer, clear any existing row in `active_session` first
- Indexes: Add indexes on `time_entries.start` and `time_entries.task_id` for query performance

## 5. Validation & Business Rules

- **No minimum duration:** Track time entries down to the second
- **Overlapping entries allowed:** No validation to prevent overlapping time entries (user freedom)
- **Single active timer:** Only one timer can be active at a time (enforced by auto-stopping previous timer)
- **Midnight splits:** Automatic splitting of entries that cross midnight boundary
- **No export functionality:** Users can manually backup the SQLite database file if needed

## 6. Technical Stack
- **Framework:** Textual (Python)
- **Database:** SQLite3
- **Platform:** Cross-platform (Windows/macOS/Linux)
