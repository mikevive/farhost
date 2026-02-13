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
- **Interface:** Dedicated screens for managing Projects, Tasks, and Categories, accessible via vim-style commands.
- **Project/Task Workflow:** The user first navigates to a `:projects` screen. Selecting a project takes them to a dedicated `:tasks` screen showing only tasks for that project.
- **Operations:** Create, Read, Update, and Archive are available on each respective screen for:
  - Categories (on the `:categories` screen)
  - Projects (on the `:projects` screen)
  - Tasks (on the project-specific `:tasks` screen)
- **Archiving:** Projects, Tasks, and Categories are **never hard-deleted**. Instead, they are archived. Archived entities:
  - Are hidden from active list views and selection dropdowns.
  - Remain linked to historical time entries, so reports are never broken.
  - Can be viewed on a dedicated archive screen accessible via `A` (Shift+a) from the respective management screen (e.g., pressing `A` on `:projects` shows archived projects).
  - Can be **restored** from the archive screen back to active status.
- **Time Entries:**
  - Users can edit any past time entry (modify start/end times, change category/task/project).
  - Users can **hard-delete** any time entry (permanent removal) for correcting mistakes.
  - Allow overlapping entries without validation (user freedom).

### D. Daily Reporting
- **Goal:** Real-time visibility into the current day's productivity
- **Daily Log:** A chronological list of all completed time entries for the selected date
- **Daily Totals:** Sum of hours grouped by Project and Category for the selected date (00:00:00 to 23:59:59)
- **Historical Navigation:** Users can navigate to past and future days using keyboard shortcuts (`h` / `l` or left/right arrows). Defaults to "Today" on open.
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
  - `:projects` or `:p` - Open projects management screen
  - `:categories` or `:c` - Open categories management screen
  - `:quit` or `:q` - Exit application

### B. Keyboard Shortcuts
- **Philosophy:** Vim-inspired keybindings throughout the application
- **Navigation:** `hjkl` for movement (left, down, up, right)
- **Actions:**
  - `a` - Open "Add" modal
  - `e` - Open "Edit" modal for the selected item
  - `d` - Archive the selected item (Projects/Tasks/Categories) or hard-delete (Time Entries)
  - `A` (Shift+a) - Toggle archive view on management screens (Projects/Tasks/Categories)
  - `r` - Restore the selected item (only available in archive view)
- **Cancel/Back:** `Esc` key to close modals or go back
- **Quit:** `:q` command

### C. Modals
All Create, Edit, Archive, and Delete operations are handled via modal dialogs to provide a clear and consistent user experience.

- **Create/Edit:** A modal prompts the user for the necessary information (e.g., name).
- **Archive (Projects/Tasks/Categories):** A modal asks for confirmation before archiving an item.
- **Delete (Time Entries only):** A modal asks for confirmation before permanently deleting an entry.
- **Restore:** A modal asks for confirmation before restoring an archived item.
- **Buttons:** Modals include clear action buttons like `[Save]`, `[Archive]`, `[Delete]`, `[Restore]`, and `[Cancel]`.

### D. UI Wireframes

#### Timer View (`:timer`)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│   Project:   [ App-Redesign      ▼]                                          │
│   Task:      [ API Integration   ▼]                                          │
│   Category:  [ Code              ▼]                                          │
│                           [   START TIMER   ]                                │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │ App-Redesign | API Integration | Code         01:23:45 | [Running]   │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────────────────┤
│ :timer | Daily (:d) | Weekly (:w) | Projects (:p) | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘

```

#### Daily Report View (`:daily`)

```

┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Daily Report (Today: 2023-10-27)                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│   Daily Log:                                                                 │
│   - 09:00 - 10:30 | App-Redesign  | UI Mockups    | Design       | 01:30:00  │
│   - 10:30 - 12:00 | Personal-Site | Blog Post     | Content      | 01:30:00  │
│   - 13:00 - 15:00 | App-Redesign  | API Login     | Code         | 02:00:00  │
│                                                                              │
│   Totals by Project:                                                         │
│   - App-Redesign:  03:30:00                                                  │
│   - Personal-Site: 01:30:00                                                  │
│                                                                              │
│   Totals by Category:                                                        │
│   - Design:        01:30:00                                                  │
│   - Content:       01:30:00                                                  │
│   - Code:          02:00:00                                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timer (:t) | :daily | Weekly (:w) | Projects (:p) | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘

```

#### Weekly Report View (`:weekly`)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Weekly Report (Week 43: Oct 23 - Oct 29) ◄ Today ►                 │
├──────────────────────────────────────────────────────────────────────────────┤
│   Mon (23): ████████████ (6.0h)                                              │
│   Tue (24): ████████████████ (8.0h)                                          │
│   Wed (25): ██████████ (5.0h)                                                │
│   Thu (26): ██████████████ (7.5h)                                            │
│   Fri (27): █████ (2.5h)                                                     │
│   Sat (28):                                                                  │
│   Sun (29):                                                                  │
│                                                                              │
│   Total Hours: 29.0h                                                         │
│                                                                              │
│   Breakdown by Project:                                                      │
│   - App-Redesign:  15.0h                                                     │
│   - Personal-Site: 14.0h                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timer (:t) | Daily (:d) | :weekly | Projects (:p) | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘

```

#### Projects View (`:projects`)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Projects                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│   > App-Redesign    (Select to view tasks)                                   │
│     Personal-Site                                                            │
│     Client-ABC                                                               │
│                                                                              │
│   (a)dd, (e)dit, (d) archive, (A) view archive                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timer (:t) | Daily (:d) | Weekly (:w) | :projects | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Create/Edit Modal (Example for Project)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Projects                                                           │
├───────── --------------------------------------------------------------------┤
│   > App-Rede│          ┌──────────────────────────────────┐                  │
│     Person  │          │ Edit Project                     │                  │
│     Client  │          ├──────────────────────────────────┤                  │
│             │          │ Name: [ App-Redesign_          ] │                  │
│             │          │                                  │                  │
│   (a)dd, (  │          │         [Save]   [Cancel]        │                  │
├───────────  │          └──────────────────────────────────┘                  │
│ Timer (:t)  | Daily (:d) | Weekly (:w) | :projects | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Delete Confirmation Modal (Example)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Projects                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│   > App-Rede│          ┌──────────────────────────────────┐                  │
│     Person  │          │ Confirm Delete                   │                  │
│     Client  │          ├──────────────────────────────────┤                  │
│             │          │ Are you sure you want to delete  │                  │
│             │          │ "App-Redesign"?                  │                  │
│             │          │                                  │                  │
│   (a)dd, (  │          │        [Delete]   [Cancel]       │                  │
├───────────  │          └──────────────────────────────────┘                  │
│ Timer (:t) | Daily (:d) | Weekly (:w) | :projects | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Tasks View (Navigated from Projects)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Tasks for "App-Redesign"                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│   > API Integration                                                          │
│     UI Mockups                                                               │
│     API Login                                                                │
│                                                                              │
│   (a)dd, (e)dit, (d) archive, (A) view archive                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timer (:t) | Daily (:d) | Weekly (:w) | Projects (:p) | Categories (:c) | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘

```

#### Categories View (`:categories`)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ DevFlow - Categories                                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│   > Code                                                                     │
│     Document                                                                 │
│     Distraction                                                              │
│     Meeting                                                                  │
│     Design                                                                   │
│     Content                                                                  │
│                                                                              │
│   (a)dd, (e)dit, (d) archive, (A) view archive                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timer (:t) | Daily (:d) | Weekly (:w) | Projects (:p) | :categories | Quit (:q)│
└──────────────────────────────────────────────────────────────────────────────┘

```

### E. Startup Behavior
- **Default View:** Timer view (main screen)
- **Database Check:** Verify database exists at `~/.farhost/devflow/devflow.db`, create if missing
- **Active Session Check:** Check for active timer in `active_session` table

### F. Crash Recovery
- **Behavior:** If app crashes while a timer is running:
  - On restart, detect the orphaned active session
  - Automatically stop the timer at the crash time (based on last known state)
  - Save the entry to `time_entries`
  - Clear the `active_session` table
  - No user prompt needed - handle automatically

### G. Headless Operations / CLI
To support integrations and scripting, the application must provide modes that do not launch the full TUI.

- **Status Output:**
  - A command-line flag (e.g., `devflow --status`) shall be implemented.
  - When invoked, the application will check for an `active_session`.
  - If a session is active, it will print the timer details to `stdout` in a single, parsable line and exit.
    - **Format:** `Project Name > Task Name > Category Name | HH:MM:SS`
  - If no session is active, it will print a concise status like `Timer Stopped` and exit.
  - The running timer `HH:MM:SS` should reflect the current elapsed time.

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
- **Archive, not delete:** Projects, Tasks, and Categories are archived (never hard-deleted). Only time entries can be permanently deleted.
- **No export functionality:** Users can manually backup the SQLite database file if needed

## 6. Technical Stack
- **Framework:** Textual (Python)
- **Database:** SQLite3
- **Platform:** Cross-platform (Windows/macOS/Linux)

## 7. Integrations

### A. Tmux Plugin
**Goal:** Integrate DevFlow seamlessly into a tmux workflow, providing at-a-glance status and quick access via a dedicated plugin.

#### 1. Status Bar Component
- **Functionality:** Display the currently running timer directly in the tmux status bar (e.g., in `status-right`).
- **Implementation:**
  - The plugin will periodically execute the `devflow --status` command.
  - The output will be displayed in the status bar, providing a real-time view of the active task without needing the main application window to be open.
  - **Example Display (Running):** `App-Redesign > API Integration > Code | 01:23:45`
  - **Example Display (Stopped):** `Timer Stopped`

#### 2. Floating Window Toggle
- **Functionality:** A dedicated tmux keybinding (e.g., `prefix + T`) will toggle a floating window that runs the main DevFlow TUI application.
- **Behavior:**
  - When the keybinding is pressed and the window is not open, a new centered, floating tmux window will be created, launching the `devflow` application inside it.
  - If the window is already open, pressing the keybinding again will close it.
