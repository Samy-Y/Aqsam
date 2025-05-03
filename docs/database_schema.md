# Aqsam Database Schema (v1)

| Table       | Purpose | Key Columns / Notes |
|-------------|---------|---------------------|
| **user**      | Base account info (all roles) | `id`, `username`, `password_hash`, `role`, profile fields |
| **student**   | Extra fields for students     | PK/FK `id` → user, `class_id` |
| **teacher**   | Extra fields for teachers     | PK/FK `id` → user, `subject_id`, `class_id` |
| **writer**    | Grants article‑writing power  | PK/FK `id` → user |
| **class**     | School class / section        | `id`, `name` (e.g. 1A), `level` |
| **subject**   | Teachable subject             | `id`, `name` |
| **grade**     | Student’s grade in a subject  | `id`, `student_id`, `subject_id`, `grade`, `date`, `comment` |
| **article**   | Markdown article for blog     | `id`, `title`, `author_id`, `content_md`, `created_at`, `last_edited`, `is_published` |

## Relationships
- **One‑to‑one:** `user` → `student|teacher|writer` (same primary key)
- **Many‑to‑one:**  
  - `student.class_id` → **class**  
  - `grade.student_id` → **student**  
  - `grade.subject_id` → **subject**  
  - `article.author_id` → **writer**
### Many‑to‑Many Links
- **teacher ⇄ subject** (`teacher_subject`)
- **teacher ⇄ class**   (`teacher_class`)
| Junction Table | Columns                       | Purpose                          |
|----------------|-------------------------------|----------------------------------|
| teacher_subject| `teacher_id`, `subject_id`    | Teacher can teach multiple subjects; subject can have multiple teachers |
| teacher_class  | `teacher_id`, `class_id`      | Teacher can teach multiple classes; class can have multiple teachers    |

> Future: if teachers can teach *multiple* classes / subjects, add junction tables `teacher_class` and `teacher_subject`.

---

_Last updated: **May 3 2025**_
