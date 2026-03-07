# הפעלת הפרויקט

## פיתוח מקומי (ללא Docker)

### דרישות מקדימות
- Python 3.9+
- Node.js 18+
- venv מותקן ב-`.venv/` בשורש הפרויקט

### הפעלה

פתח שני טרמינלים:

**טרמינל 1 — Backend:**
```bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
```

**טרמינל 2 — Frontend:**
```bash
cd frontend
npm run dev
```

האפליקציה זמינה בכתובת: http://localhost:3000

### עצירה
```bash
lsof -ti:8000,3000 | xargs kill -9
```

---

## Docker (פרודקשן)

### דרישות מקדימות
יש להפעיל את Docker Desktop לפני הרצת הסקריפטים:
```bash
open -a Docker
```
יש להמתין כ-30 שניות עד שה-daemon פועל.

### הפעלה
```bash
bash scripts/start.sh
```

הפרויקט בנוי כקונטיינר אחד: ה-frontend נבנה סטטית ומוגש על ידי ה-backend.

האפליקציה זמינה בכתובת: http://localhost:8000

### עצירה
```bash
bash scripts/stop.sh
```

---

## כניסה למערכת

- שם משתמש: `user`
- סיסמה: `password`

---

## הרצת בדיקות Backend

```bash
source .venv/bin/activate
cd backend
python -m pytest test_main.py -v
```
