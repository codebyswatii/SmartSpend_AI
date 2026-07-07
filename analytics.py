from db import get_all_expenses

def generate_insights(owner_id):
    
    data = get_all_expenses(owner_id)

    if not data:
        return ({
        "total_spent": 0,
        "category_distribution": {},
        "insights": []
    })

    total = 0
    category_sum = {}

    for row in data:
        try:
            amount = int(row[3])
        except:
            amount = 0
    
        category = row[4]

        total += amount

        if category not in category_sum:
            category_sum[category] = 0

        category_sum[category] += amount

    # Calculate percentages
    result = {}
    insights = []

    for cat, amt in category_sum.items():
        percent = (amt / total) * 100 if total != 0 else 0
        result[cat] = round(percent, 2)

        if percent > 50:
            insights.append(f"High spending on {cat}")
        elif percent > 30:
            insights.append(f"Moderate spending on {cat}")
        else:
            insights.append(f"Low spending on {cat}")

    # 🔥 Anomaly Detection (NEW CODE)
    # for row in data:
    #     amount = row[2]
        
    #     if amount > 2000:
    #         insights.append(f"Unusually high expense detected: ₹{amount}")
    # 🔥 Smarter Anomaly Detection
    amounts = [int(row[3]) if str(row[3]).isdigit() else 0 for row in data]
    avg = sum(amounts) / len(amounts)

    for row in data:
        amount = int(row[3])
        
        if amount > avg * 2:
            insights.append(f"Unusual high expense detected: ₹{amount}")

    if "bills" in result and result["bills"] > 50:
            insights.append("High fixed expenses may reduce savings")

    return ({
        "total_spent": total,
        "category_distribution": result,
        "insights": insights
    })
