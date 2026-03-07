<!--

# High level steps for project

Part 1: Plan

Enrich this document to plan out each of these parts in detail, with substeps listed out as a checklist to be checked off by the agent, and with tests and success critieria for each. Also create an AGENTS.md file inside the frontend directory that describes the existing code there. Ensure the user checks and approves the plan.

Part 2: Scaffolding

Set up the Docker infrastructure, the backend in backend/ with FastAPI, and write the start and stop scripts in the scripts/ directory. This should serve example static HTML to confirm that a 'hello world' example works running locally and also make an API call.

Part 3: Add in Frontend

Now update so that the frontend is statically built and served, so that the app has the demo Kanban board displayed at /. Comprehensive unit and integration tests.

Part 4: Add in a fake user sign in experience

Now update so that on first hitting /, you need to log in with dummy credentials ("user", "password") in order to see the Kanban, and you can log out. Comprehensive tests.

Part 5: Database modeling

Now propose a database schema for the Kanban, saving it as JSON. Document the database approach in docs/ and get user sign off.

Part 6: Backend

Now add API routes to allow the backend to read and change the Kanban for a given user; test this thoroughly with backend unit tests. The database should be created if it doesn't exist.

Part 7: Frontend + Backend

Now have the frontend actually use the backend API, so that the app is a proper persistent Kanban board. Test very throughly.

Part 8: AI connectivity

Now allow the backend to make an AI call via OpenRouter. Test connectivity with a simple "2+2" test and ensure the AI call is working.

Part 9: Now extend the backend call so that it always calls the AI with the JSON of the Kanban board, plus the user's question (and conversation history). The AI should respond with Structured Outputs that includes the response to the user and optionaly an update to the Kanban. Test thoroughly.

Part 10: Now add a beautiful sidebar widget to the UI supporting full AI chat, and allowing the LLM (as it determines) to update the Kanban based on its Structured Outputs. If the AI updates the Kanban, then the UI should refresh automatically.
-->


להלן גרסה מעודכנת ל־`docs/PLAN.md`, באותו מבנה רעיוני — אך ללא צ'קבוקסים וללא רשימות סימון.

---

# PLAN.md

## סטטוס נוכחי

| חלק | נושא | סטטוס |
|-----|------|-------|
| 1 | תכנון | הושלם |
| 2 | Docker + Backend בסיסי | הושלם |
| 3 | Frontend סטטי | הושלם |
| 4 | התחברות | הושלם |
| 5 | מודל DB | הושלם |
| 6 | Backend API | הושלם |
| 7 | Frontend + Backend | הושלם |
| 8 | חיבור AI | הושלם |
| 9 | Structured Outputs | הושלם |
| 10 | ממשק צ'אט | הושלם |

---

## מטרת המסמך

מסמך זה מגדיר תכנית עבודה מדורגת וברורה לבניית MVP של אפליקציית ניהול פרויקטים (Kanban + AI), בהתאם לדרישות המערכת ולהחלטות הטכנולוגיות.

כל שלב כולל:

* פירוט משימות
* בדיקות נדרשות
* קריטריוני הצלחה

אין להתחיל שלב לפני שהשלב הקודם הושלם ועומד בקריטריוני ההצלחה.

אין להתחיל מימוש לפני אישור מפורש של המשתמש למסמך זה.

---

# חלק 1: תכנון

## מטרה

להעשיר את המסמך כך שכל אחד מהחלקים יפורק לתת־שלבים ברורים עם בדיקות וקריטריוני הצלחה. בנוסף, ליצור קובץ `AGENTS.md` בתוך תיקיית `frontend` המתאר את הקוד הקיים שם. יש לוודא שהמשתמש בודק ומאשר את התכנית לפני המשך.

## פירוט עבודה

יש לבצע ניתוח של המצב הקיים בתיקיית `frontend`, להבין את מבנה הרכיבים, ניהול ה-state, מנגנון ה-drag and drop, והיכן יש נקודות חיבור עתידיות ל-Backend.

יש ליצור קובץ `frontend/AGENTS.md` שיכלול:

* תיאור ארכיטקטורת ה-Frontend
* פירוט מבנה תיקיות
* תיאור רכיבי Kanban
* תיאור מנגנון ניהול state
* תלויות חיצוניות
* נקודות התאמה נדרשות לצורך חיבור ל-Backend

יש להרחיב את תכנית העבודה עבור כל אחד מהשלבים 2–10, כולל בדיקות וקריטריוני הצלחה ברורים ומדידים.

## בדיקות

המסמך צריך להיות חד־משמעי, ללא שלבים עמומים. כל שלב חייב להיות ניתן לבדיקה עצמאית.

## קריטריון הצלחה

אישור מפורש של המשתמש לתכנית לפני תחילת מימוש.

---

# חלק 2: תשתית Docker ו-Backend בסיסי

## מטרה

להקים תשתית Docker מלאה, ליצור backend בתיקיית `backend/` באמצעות FastAPI, לכתוב סקריפטי start/stop בתיקיית `scripts/`, ולהגיש דוגמת HTML סטטית יחד עם קריאת API לבדיקת תקינות.

## פירוט עבודה

יש ליצור Dockerfile המשתמש ב-uv כמנהל חבילות Python, מתקין FastAPI ו-Uvicorn, חושף פורט מתאים ומשתמש בקובץ `.env`.

יש להקים מבנה בסיסי בתיקיית `backend/`, כולל `app/main.py`, ולהגדיר endpoint בנתיב `/` שמחזיר HTML פשוט (hello world) ו-endpoint נוסף בנתיב `/api/health` שמחזיר JSON תקין.

יש ליצור סקריפטים להפעלה וכיבוי שרת עבור Mac/Linux (sh) ועבור Windows (bat).

## בדיקות

יש לוודא ש־docker build מצליח, שהקונטיינר עולה, שגישה ל־localhost מציגה HTML תקין, ושקריאה ל־/api/health מחזירה JSON תקין.

## קריטריון הצלחה

המערכת רצה מקומית בתוך Docker ומחזירה גם דף HTML וגם תגובת API תקינה.

## החלטות מימוש

- Dockerfile משתמש ב-`uv` כמנהל חבילות Python
- Backend: FastAPI + Uvicorn, קובץ `.env` נקרא עם `python-dotenv`
- `GET /api/health` מחזיר `{"status": "ok"}`
- סקריפטים: `scripts/start.sh`, `scripts/stop.sh`, `scripts/start.bat`, `scripts/stop.bat`
- קונטיינר חושף פורט 8000

---

# חלק 3: שילוב Frontend סטטי

## מטרה

לבנות את NextJS בצורה סטטית ולהגיש אותו דרך FastAPI כך שבלחיצה על `/` יוצג לוח הקנבן מהדמו הקיים.

## פירוט עבודה

יש להוסיף שלב build ל-Docker, להעתיק את תוצרי ה-build לתיקייה סטטית, ולהגדיר ב-FastAPI הגשת קבצים סטטיים וניתוב מתאים ל־/ כך שכל הראוטים יעבדו.

## בדיקות

יש לוודא ש־docker run מציג את לוח הקנבן, שמנגנון drag and drop עובד, שאין שגיאות בקונסול, ושבדיקות יחידה ואינטגרציה בסיסיות עוברות.

## קריטריון הצלחה

לוח הקנבן מוצג ב־/ מתוך Docker ופועל כפי שפעל בדמו המקורי.

## החלטות מימוש

- Next.js עם `output: 'export'` — build סטטי בלבד (ללא SSR)
- `BUILD_EXPORT=1 npm run build` מייצר תיקיית `out/`
- FastAPI מגיש קבצים סטטיים ומטפל ב-catch-all לתמיכה בניתוב client-side
- dev mode: `npm run dev` על פורט 3000 עם proxy ל-8000
- הקבצים הסטטיים של פרודקשן נשמרים בתיקיית `static/` בשורש

---

# חלק 4: התחברות מזויפת

## מטרה

להוסיף חוויית התחברות בסיסית עם credentials קשיחים ("user", "password"), אפשרות logout, והגנה על הנתיב הראשי.

## פירוט עבודה

יש ליצור מסך login, לבדוק credentials קשיחים, לשמור session פשוט (למשל באמצעות cookie), להגן על `/`, ולהוסיף כפתור logout.

## בדיקות

יש לוודא שלא ניתן לראות את הקנבן ללא login, ש-login שגוי נכשל, ש-login תקין מציג את הקנבן, וש-logout מחזיר למסך ההתחברות.

## קריטריון הצלחה

חוויית התחברות מלאה ופשוטה עובדת מקצה לקצה.

## החלטות מימוש

- cookie בשם `session` עם ערך `1`, עם דגל `httponly`
- credentials קשיחים ב-`main.py`: `VALID_USER="user"`, `VALID_PASS="password"`
- frontend: `POST /api/login` עם `credentials: "include"`, redirect ל-`/login` בקוד 401
- backend: redirect מ-`/` ל-`/login` לגישה ללא cookie; `POST /api/logout` מוחק את ה-cookie
- אין middleware (לא תואם `output: export`) — הגנה מתבצעת ב-`useEffect` בצד client

---

# חלק 5: מודל בסיס נתונים

## מטרה

להציע schema לבסיס הנתונים עבור Kanban, לשמור את הלוח כ-JSON, ולתעד את הגישה בתיקיית `docs/`. יש לקבל אישור משתמש לפני המשך.

## פירוט עבודה

יש לתכנן טבלת users וטבלת boards, כאשר תוכן הלוח נשמר כ-JSON. יש לתעד את ההחלטות הארכיטקטוניות במסמך ייעודי ב-`docs/`.

## בדיקות

יש לוודא שה-schema ברור, פשוט, תואם לדרישות ה-MVP, וניתן להרחבה בעתיד.

## קריטריון הצלחה

אישור מפורש של המשתמש על המודל המוצע.

## החלטות מימוש

- טבלה אחת בלבד: `boards` עם עמודות `user_id` (TEXT) ו-`data` (TEXT/JSON)
- אין טבלת users ל-MVP — `user_id` הוא מחרוזת קשיחה `"user"`
- כל תוכן הלוח נשמר כ-JSON blob אחד — פשוט ומספיק ל-MVP
- DB נוצר אוטומטית ב-`backend/kanban.db` עם `CREATE TABLE IF NOT EXISTS`
- מתועד ב-`docs/database.md`

---

# חלק 6: מימוש Backend מלא

## מטרה

להוסיף API המאפשר קריאה ושינוי של לוח הקנבן עבור משתמש נתון, כולל יצירת SQLite אם אינו קיים.

## פירוט עבודה

יש לממש יצירה אוטומטית של בסיס הנתונים, endpoint לשליפת לוח (`GET /api/board`) ו-endpoint לעדכון לוח (`PUT /api/board`), כולל בדיקות יחידה ל-backend.

## בדיקות

יש לוודא שהנתונים נשמרים בפועל ב-SQLite, ששליפה מחזירה JSON תקין, ושכל בדיקות ה-backend עוברות.

## קריטריון הצלחה

API יציב, מתועד ונבדק היטב.

## החלטות מימוש

- `backend/app/database.py`: `init_db()`, `get_board(user_id)`, `save_board(user_id, data)`
- `init_db()` נקרא אוטומטית ב-`lifespan` וגם בעת import
- `GET /api/board` — מחזיר JSON של הלוח, דורש auth
- `PUT /api/board` — מקבל JSON מלא של הלוח ומחליף את הקיים, דורש auth
- אין CRUD granular — כל שינוי מחליף את כל ה-blob
- 7 בדיקות backend עוברות

---

# חלק 7: חיבור מלא בין Frontend ל-Backend

## מטרה

להחליף את ה-state המקומי ב-Frontend בקריאות API אמיתיות כך שהלוח יהיה persistent.

## פירוט עבודה

יש לעדכן את ה-Frontend כך שיטען את הלוח מה-Backend בעת טעינה ראשונית, וישמור שינויים דרך ה-API. יש לטפל במצבי טעינה ושגיאות.

## בדיקות

יש לוודא ששינויים נשמרים, שרענון דף שומר על state, ושבדיקות אינטגרציה מלאות עוברות.

## קריטריון הצלחה

לוח קנבן persistent אמיתי שעובד מקצה לקצה.

## החלטות מימוש

- `KanbanBoard.tsx`: טוען מ-`GET /api/board` ב-`useEffect` בטעינה ראשונה
- שמירה אוטומטית ב-`useEffect` על כל שינוי ב-`board` state (עם `useRef` למניעת שמירה ראשונה)
- `credentials: "include"` בכל קריאות ה-fetch
- dev mode: `next.config.ts` מגדיר rewrites proxy מ-`/api/*` ל-`http://localhost:8000`
- production/Docker: frontend נבנה סטטית עם `BUILD_EXPORT=1` ומוגש ישירות מ-FastAPI
- 9 בדיקות backend עוברות

---

# חלק 8: חיבור ל-AI דרך OpenRouter

## מטרה

לאפשר ל-Backend לבצע קריאה ל-AI באמצעות OpenRouter ולוודא תקשורת תקינה באמצעות בדיקת "2+2".

## פירוט עבודה

יש ליצור route ייעודי לבדיקת AI, להשתמש במודל `openai/gpt-oss-120b`, ולשלוף את `OPENROUTER_API_KEY` מקובץ `.env`.

## בדיקות

יש לוודא שמתקבלת תשובה תקינה, שטיפול בשגיאות עובד, ושהמערכת מתמודדת עם timeout.

## קריטריון הצלחה

קריאת AI עובדת בצורה יציבה ומחזירה תשובה תקינה.

## החלטות מימוש

- `backend/app/ai.py`: פונקציה `call_ai(messages)` ופונקציה פנימית `_call(url, api_key, model, messages)`
- מנסה OpenRouter ראשון (מודל `openai/gpt-oss-120b`, מפתח `OPEN_ROUTE_API_KEY`)
- fallback אוטומטי ל-OpenAI (מודל `gpt-4o-mini`, מפתח `OPENAI_API_KEY`) בשגיאות 401/402/403
- `GET /api/ai/test` — endpoint לבדיקה שמחזיר `{"answer": "4"}` לשאלת 2+2
- בדיקות עם `unittest.mock.patch` — לא דורשות API key אמיתי
- 9 בדיקות backend עוברות

---

# חלק 9: Structured Outputs ועדכון Kanban

## מטרה

להרחיב את קריאת ה-AI כך שתישלח גם גרסת JSON מלאה של הלוח, יחד עם שאלת המשתמש והיסטוריית השיחה, וה-AI יחזיר תגובה מובנית הכוללת תשובה למשתמש ואופציונלית עדכון ללוח.

## פירוט עבודה

יש להגדיר schema ברור לתגובה מובנית, לבצע parsing בצד ה-Backend, לעדכן את בסיס הנתונים במידת הצורך, ולהחזיר למשתמש גם תשובה טקסטואלית וגם סטטוס עדכון.

## בדיקות

יש לוודא שה-AI מחזיר JSON תקין בהתאם ל-schema, שעדכון לוח מתבצע כראוי, ושמקרים חריגים מטופלים.

## קריטריון הצלחה

ה-AI מסוגל להשיב למשתמש ולעדכן את הלוח בצורה מבוקרת ויציבה.

## החלטות מימוש

- `POST /api/chat` מקבל `{ messages: [...], board: {...} }` — הלוח נשלח מה-frontend
- system prompt מסביר את מבנה הלוח ומבקש תגובת JSON בפורמט `{"reply": "...", "board_update": null | {...}}`
- `ChatRequest` ו-`ChatMessage` מוגדרים כ-Pydantic models
- הלוח הנוכחי מוטמע בתוך ה-system prompt עצמו
- אם `board_update` קיים — נשמר מיד ב-DB דרך `save_board`
- parsing סלחני: אם ה-AI החזיר markdown fences נגרד אותן; אם ה-JSON לא תקין — מחזירים את הטקסט כ-reply ו-null כ-board_update
- 3 בדיקות חדשות; סך הכל 12 בדיקות backend עוברות

---

# חלק 10: ממשק צ'אט מלא ב-UI

## מטרה

להוסיף Sidebar מעוצב לצ'אט AI, לאפשר שיחה מלאה, ולעדכן את הלוח אוטומטית אם ה-AI מחזיר שינוי.

## פירוט עבודה

יש ליצור קומפוננטת Sidebar ייעודית, לחבר אותה ל-API, להציג היסטוריית שיחה, ולרענן את ה-UI אוטומטית לאחר עדכון לוח.

## בדיקות

יש לוודא שהצ'אט עובד, שה-AI יכול לעדכן לוח, שה-UI מתרענן אוטומטית, ושבדיקות אינטגרציה מלאות עוברות.

## קריטריון הצלחה

צ'אט AI מלא, יציב ומשולב בלוח הקנבן.

## החלטות מימוש

- `AIChatSidebar.tsx`: קומפוננטה עם sidebar קבוע בצד ימין (340px)
- board state הועלה ל-`page.tsx` — מועבר כ-props גם ל-`KanbanBoard` וגם ל-`AIChatSidebar`
- `KanbanBoard.tsx`: מקבל `board` ו-`setBoard` כ-props; הסרנו fetch פנימי של טעינה; שמירה על שינויים נשארת בקומפוננטה
- היסטוריית שיחה מנוהלת ב-state מקומי של `AIChatSidebar`
- אם `board_update` מוחזר מה-API — `setBoard` נקרא ישירות ומרענן את הלוח אוטומטית
- Enter שולח הודעה (Shift+Enter = שורה חדשה)
- אינדיקטור טעינה (3 נקודות מקפצות) בזמן המתנה לתגובה
- `KanbanBoard.test.tsx` עודכן עם `Wrapper` component שמספק state אמיתי
- 6 בדיקות frontend עוברות

---

# אישור נדרש

לפני תחילת מימוש:

יש לאשר במפורש שהמסמך ברור, מלא, ואין שלבים חסרים.

לא תתבצע כל עבודה טכנית לפני קבלת אישור מפורש.
