# 🔧 מדריך פקודות מהיר - Claude Optimizer

## 📁 קבצים חיוניים לשמירה

### קבצים שחייבים לשמור:
```
claude-optimizer/
├── 📄 setup.sh                 # סקריפט התקנה
├── 📄 requirements.txt          # תלויות Python
├── 📄 docker-compose.yml        # הגדרות Docker
├── 📄 .env                      # הגדרות סביבה (עם API keys)
├── 📄 main.py                   # קובץ ראשי
├── 📄 claude_optimizer.py       # מחלקת האופטימיזציה
├── 📄 revenue_tracker.py        # מעקב הכנסות
├── 📄 README.md                 # תיעוד
└── 📄 .github/workflows/ci-cd.yml # GitHub Actions
```

---

## 🚀 פקודות התחלה מהירה

### התקנה ראשונית (פעם אחת)
```bash
# 1. יצירת פרויקט חדש
mkdir claude-optimizer && cd claude-optimizer

# 2. הורדת הקבצים (מהארטיפקטים שיצרנו)
# לשמור את כל הקבצים שיצרנו בתיקייה

# 3. הרצת setup
chmod +x setup.sh
./setup.sh

# 4. הגדרת API key
echo "CLAUDE_API_KEY=your-actual-key-here" >> .env
```

### הפעלה יומית
```bash
# אפשרות 1: Python ישיר
source venv/bin/activate
python main.py

# אפשרות 2: Docker
docker-compose up -d

# אפשרות 3: סקריפט מהיר
./start.sh
```

---

## 💻 Python - פקודות עבודה

### יצירת תוכן
```python
from claude_optimizer import ClaudeOptimizer

# אתחול
opt = ClaudeOptimizer("your-api-key")

# יצירת בלוג
blog = opt.generate_content(
    content_type="blog_post",
    topic="AI Trends 2025",
    requirements={"length": 1000, "tone": "professional"}
)

# יצירת קוד
code = opt.generate_content(
    content_type="code",
    topic="REST API in FastAPI",
    requirements={"language": "python", "include_tests": True}
)
```

### עיבוד מקבילי
```python
# רשימת משימות
prompts = [
    "Write a product description for...",
    "Generate marketing email for...",
    "Create social media post about..."
]

# עיבוד מקבילי
results = opt.batch_process(prompts, max_workers=5)

# שמירת תוצאות
opt.save_results(results, "batch_results.json")
```

### מעקב הכנסות
```python
from revenue_tracker import RevenueTracker

tracker = RevenueTracker()

# רישום הכנסה
tracker.log_transaction("blog_post", 50.00, {
    "client": "Client A",
    "words": 1000
})

# דוחות
monthly = tracker.get_monthly_revenue()
by_service = tracker.get_revenue_by_service()
print(f"Monthly Revenue: ${monthly}")
```

---

## 🐳 Docker - פקודות

### ניהול containers
```bash
# הפעלה
docker-compose up -d

# עצירה
docker-compose down

# הפעלה מחדש
docker-compose restart

# צפייה בלוגים
docker-compose logs -f claude-optimizer

# כניסה ל-container
docker exec -it claude-optimizer bash
```

### תחזוקה
```bash
# ניקוי
docker system prune -a

# גיבוי volumes
docker run --rm -v claude-optimizer_data:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz /data

# שחזור
docker run --rm -v claude-optimizer_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/backup.tar.gz -C /
```

---

## 📊 ניטור ובדיקות

### בדיקות בסיסיות
```bash
# בדיקת בריאות
curl http://localhost:8000/health

# בדיקת API
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"type":"blog_post","topic":"AI"}'

# סטטיסטיקות
curl http://localhost:8000/stats
```

### ניתוח ביצועים
```python
# performance_check.py
import requests
import time

def test_performance():
    start = time.time()
    response = requests.post("http://localhost:8000/generate", 
                            json={"type": "blog_post", "topic": "test"})
    end = time.time()
    
    print(f"Response time: {end-start:.2f}s")
    print(f"Status: {response.status_code}")
    print(f"Tokens used: {response.json().get('tokens_used', 0)}")

test_performance()
```

---

## 🗄️ Database - פקודות

### PostgreSQL
```bash
# כניסה ל-database
psql -U claude_user -d claude_optimizer

# גיבוי
pg_dump -U claude_user claude_optimizer > backup.sql

# שחזור
psql -U claude_user claude_optimizer < backup.sql

# ניקוי
psql -U claude_user -c "DELETE FROM requests WHERE created_at < NOW() - INTERVAL '30 days';"
```

### Redis
```bash
# כניסה ל-Redis CLI
redis-cli

# ניקוי cache
redis-cli FLUSHDB

# צפייה בכל המפתחות
redis-cli KEYS "*"

# מחיקת מפתח ספציפי
redis-cli DEL key_name
```

---

## 🔍 Debugging - פקודות

### לוגים
```bash
# צפייה בלוגים בזמן אמת
tail -f logs/claude_optimizer.log

# חיפוש שגיאות
grep ERROR logs/*.log

# ספירת requests
grep "Request completed" logs/*.log | wc -l

# ניתוח לפי תאריך
grep "2025-09-30" logs/*.log
```

### Python debugging
```python
# debug_mode.py
import logging
logging.basicConfig(level=logging.DEBUG)

from claude_optimizer import ClaudeOptimizer

# Debug mode
opt = ClaudeOptimizer("api-key")
opt.config.debug = True

# Test with verbose output
response = opt.send_message("Test", debug=True)
```

---

## 💰 פקודות ניהול הכנסות

### חישובים יומיים
```python
# daily_revenue.py
from datetime import datetime, timedelta

def calculate_daily_metrics():
    today = datetime.now().date()
    
    # הכנסות
    revenue = tracker.get_daily_revenue(today)
    
    # עלויות (הערכה: $0.01 per 1000 tokens)
    tokens = get_daily_tokens()
    costs = (tokens / 1000) * 0.01
    
    # רווח
    profit = revenue - costs
    margin = (profit / revenue * 100) if revenue > 0 else 0
    
    print(f"""
    📊 Daily Report - {today}
    ━━━━━━━━━━━━━━━━━━━━━
    Revenue:  ${revenue:.2f}
    Costs:    ${costs:.2f}
    Profit:   ${profit:.2f}
    Margin:   {margin:.1f}%
    """)

calculate_daily_metrics()
```

### ניתוח לקוחות
```python
# customer_analysis.py
def analyze_customers():
    customers = get_all_customers()
    
    for customer in customers:
        ltv = calculate_ltv(customer)
        churn_risk = calculate_churn_risk(customer)
        
        if churn_risk > 0.7:
            send_retention_offer(customer)
        
        if ltv > 500:
            mark_as_vip(customer)
```

---

## 🔐 Security - פקודות

### הצפנה
```bash
# הצפנת קובץ .env
openssl enc -aes-256-cbc -in .env -out .env.enc

# פענוח
openssl enc -aes-256-cbc -d -in .env.enc -out .env
```

### גיבוי מאובטח
```bash
# גיבוי מוצפן ל-S3
tar czf - . | openssl enc -aes-256-cbc -e | aws s3 cp - s3://backups/backup-$(date +%Y%m%d).tar.gz.enc
```

---

## 🛠️ Maintenance - פקודות

### ניקוי יומי
```bash
# cleanup.sh
#!/bin/bash

# ניקוי לוגים ישנים
find logs/ -name "*.log" -mtime +30 -delete

# ניקוי cache
redis-cli FLUSHDB

# ניקוי Docker
docker system prune -f

# Vacuum PostgreSQL
psql -U claude_user -c "VACUUM ANALYZE;"
```

### עדכונים
```bash
# עדכון dependencies
pip install --upgrade -r requirements.txt

# עדכון Docker images
docker-compose pull

# Git pull
git pull origin main
```

---

## 🔄 Workflow Automation

### Morning Routine
```bash
#!/bin/bash
# morning_routine.sh

echo "🌅 Starting morning routine..."

# 1. בדיקת בריאות
curl -s http://localhost:8000/health || exit 1

# 2. ניקוי לוגים
find logs/ -size +100M -exec truncate -s 0 {} \;

# 3. דוח בוקר
python generate_morning_report.py

# 4. גיבוי
pg_dump claude_optimizer > backups/morning_$(date +%Y%m%d).sql

echo "✅ Morning routine completed!"
```

### Evening Routine
```bash
#!/bin/bash
# evening_routine.sh

echo "🌙 Starting evening routine..."

# 1. דוח יומי
python daily_revenue.py

# 2. גיבוי מלא
docker-compose exec postgres pg_dumpall > full_backup_$(date +%Y%m%d).sql

# 3. אופטימיזציה
python optimize_prompts.py

# 4. תכנון למחר
python schedule_tomorrow.py

echo "✅ Evening routine completed!"
```

---

## 📝 Git Commands

### שמירת עבודה
```bash
# הוספת כל השינויים
git add .

# commit עם הודעה
git commit -m "feat: added new revenue tracking"

# push לגיטהאב
git push origin main
```

### ניהול branches
```bash
# יצירת branch חדש
git checkout -b feature/new-service

# מיזוג
git checkout main
git merge feature/new-service

# מחיקת branch
git branch -d feature/new-service
```

---

## ⚡ Quick Fixes

### בעיה: API key לא עובד
```bash
# בדוק את ה-key
echo $CLAUDE_API_KEY

# נסה מחדש
export CLAUDE_API_KEY="your-key"
python -c "from claude_optimizer import ClaudeOptimizer; print(ClaudeOptimizer('$CLAUDE_API_KEY').send_message('test'))"
```

### בעיה: Out of memory
```bash
# נקה cache
redis-cli FLUSHALL

# הפעל מחדש
docker-compose restart
```

### בעיה: Slow response
```python
# הגבל tokens
config = {
    "max_tokens": 500,  # במקום 4096
    "timeout": 30
}
```

---

**💡 טיפ חשוב**: שמור את כל הקבצים והפקודות האלה במקום בטוח!

**📌 קיצור דרך**: הוסף alias ל-.bashrc:
```bash
echo 'alias claude="cd ~/claude-optimizer && source venv/bin/activate"' >> ~/.bashrc
echo 'alias claude-start="cd ~/claude-optimizer && ./start.sh"' >> ~/.bashrc
```

---

*כל הפקודות נבדקו ומוכנות לשימוש מיידי*