<!--
# The Project Management MVP web app

## Business Requirements

This project is building a Project Management App. Key features:
- A user can sign in
- When signed in, the user sees a Kanban board representing their project
- The Kanban board has fixed columns that can be renamed
- The cards on the Kanban board can be moved with drag and drop, and edited
- There is an AI chat feature in a sidebar; the AI is able to create / edit / move one or more cards

## Limitations

For the MVP, there will only be a user sign in (hardcoded to 'user' and 'password') but the database will support multiple users for future.

For the MVP, there will only be 1 Kanban board per signed in user.

For the MVP, this will run locally (in a docker container)

## Technical Decisions

- NextJS frontend
- Python FastAPI backend, including serving the static NextJS site at /
- Everything packaged into a Docker container
- Use "uv" as the package manager for python in the Docker container
- Use OpenRouter for the AI calls. An OPENROUTER_API_KEY is in .env in the project root
- Use `openai/gpt-oss-120b` as the model
- Use SQLLite local database for the database, creating a new db if it doesn't exist
- Start and Stop server scripts for Mac, PC, Linux in scripts/

## Starting Point

A working MVP of the frontend has been built and is already in frontend. This is not yet designed for the Docker setup. It's a pure frontend-only demo.

## Color Scheme

- Accent Yellow: `#ecad0a` - accent lines, highlights
- Blue Primary: `#209dd7` - links, key sections
- Purple Secondary: `#753991` - submit buttons, important actions
- Dark Navy: `#032147` - main headings
- Gray Text: `#888888` - supporting text, labels

## Coding standards

1. Use latest versions of libraries and idiomatic approaches as of today
2. Keep it simple - NEVER over-engineer, ALWAYS simplify, NO unnecessary defensive programming. No extra features - focus on simplicity.
3. Be concise. Keep README minimal. IMPORTANT: no emojis ever
4. When hitting issues, always identify root cause before trying a fix. Do not guess. Prove with evidence, then fix the root cause.

## Working documentation

All documents for planning and executing this project will be in the docs/ directory.
Please review the docs/PLAN.md document before proceeding.
-->


אפליקציית MVP לניהול פרויקטים (Project Management)
דרישות עסקיות

הפרויקט בונה אפליקציית ניהול פרויקטים. פיצ'רים מרכזיים:

משתמש יכול להתחבר (Sign In)

תשתמש  בטוקנים עם ספריית JWT

 יכולת להתחבר דרך google or github 

 שכחתי סיסמא לשלחיה במייל   


לאחר התחברות, המשתמש רואה לוח קנבן המייצג את הפרויקט שלו

ללוח הקנבן יש עמודות קבועות שניתן לשנות את שמן

ניתן לגרור כרטיסים בין עמודות (Drag & Drop) ולערוך אותם

קיימת תכונת צ'אט AI בסיידבר; ה-AI יכול ליצור / לערוך / להעביר כרטיס אחד או יותר

מגבלות

לצורך ה-MVP:

יש התחברות אחת בלבד עם פרטי משתמש קשיחים:
username: user
password: password
עם זאת, בסיס הנתונים יתמוך במספר משתמשים בעתיד.

לכל משתמש יש לוח קנבן אחד בלבד.

המערכת תרוץ מקומית (בתוך Docker container).

החלטות טכנולוגיות

Frontend ב-NextJS

Backend ב-Python עם FastAPI, כולל הגשת האתר הסטטי של NextJS בנתיב /

כל המערכת ארוזה בתוך Docker container אחד

שימוש ב-uv כמנהל חבילות Python בתוך ה-Docker container

שימוש ב-OpenRouter לקריאות AI

משתנה סביבה OPENROUTER_API_KEY נמצא בקובץ .env בשורש הפרויקט

שימוש במודל: openai/gpt-oss-120b

שימוש ב-SQLite כבסיס נתונים מקומי, עם יצירה אוטומטית של DB אם אינו קיים

סקריפטים להפעלה וכיבוי שרת עבור Mac, PC, Linux בתיקיית scripts/

נקודת התחלה

קיים MVP עובד של ה-Frontend בתיקיית frontend.
הוא כרגע דמו Frontend בלבד ואינו מותאם עדיין להרצה בתוך Docker או לחיבור ל-Backend.

סכמת צבעים

צהוב הדגשה (Accent Yellow): #ecad0a – קווי הדגשה, היילייטים

כחול ראשי (Blue Primary): #209dd7 – קישורים, אזורים מרכזיים

סגול משני (Purple Secondary): #753991 – כפתורי שליחה, פעולות חשובות

כחול כהה (Dark Navy): #032147 – כותרות ראשיות

טקסט אפור (Gray Text): #888888 – טקסט משני, תוויות

סטנדרטים לכתיבה וקוד

להשתמש בגרסאות הספריות העדכניות ביותר ובגישה אידיומטית עדכנית.

לשמור על פשטות – לא לבצע over-engineering, לא להוסיף הגנות מיותרות, לא להוסיף פיצ'רים שלא נדרשים. להתמקד בפשטות בלבד.

להיות תמציתיים. קובץ README מינימלי. אין להשתמש באימוג'ים כלל.

כאשר נתקלים בבעיה – תמיד לזהות את שורש הבעיה לפני תיקון. לא לנחש. להוכיח באמצעות ראיות, ואז לתקן את שורש הבעיה.

תיעוד עבודה

כל מסמכי התכנון והביצוע של הפרויקט יישמרו בתיקיית docs/.

יש לעיין במסמך docs/PLAN.md לפני תחילת עבודה.