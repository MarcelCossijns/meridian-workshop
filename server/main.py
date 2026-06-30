import math
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from mock_data import inventory_items, orders, demand_forecasts, backlog_items, spending_summary, monthly_spending, category_spending, recent_transactions, purchase_orders

app = FastAPI(title="Factory Inventory Management System")

# Quarter mapping for date filtering
QUARTER_MAP = {
    'Q1-2025': ['2025-01', '2025-02', '2025-03'],
    'Q2-2025': ['2025-04', '2025-05', '2025-06'],
    'Q3-2025': ['2025-07', '2025-08', '2025-09'],
    'Q4-2025': ['2025-10', '2025-11', '2025-12']
}

def filter_by_month(items: list, month: Optional[str]) -> list:
    """Filter items by month/quarter based on order_date field"""
    if not month or month == 'all':
        return items

    if month.startswith('Q'):
        # Handle quarters
        if month in QUARTER_MAP:
            months = QUARTER_MAP[month]
            return [item for item in items if any(m in item.get('order_date', '') for m in months)]
    else:
        # Direct month match
        return [item for item in items if month in item.get('order_date', '')]

    return items

def apply_filters(items: list, warehouse: Optional[str] = None, category: Optional[str] = None,
                 status: Optional[str] = None) -> list:
    """Apply common filters to a list of items"""
    filtered = items

    if warehouse and warehouse != 'all':
        filtered = [item for item in filtered if item.get('warehouse') == warehouse]

    if category and category != 'all':
        filtered = [item for item in filtered if item.get('category', '').lower() == category.lower()]

    if status and status != 'all':
        filtered = [item for item in filtered if item.get('status', '').lower() == status.lower()]

    return filtered

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class InventoryItem(BaseModel):
    id: str
    sku: str
    name: str
    category: str
    warehouse: str
    quantity_on_hand: int
    reorder_point: int
    unit_cost: float
    location: str
    last_updated: str

class Order(BaseModel):
    id: str
    order_number: str
    customer: str
    items: List[dict]
    status: str
    order_date: str
    expected_delivery: str
    total_value: float
    actual_delivery: Optional[str] = None
    warehouse: Optional[str] = None
    category: Optional[str] = None

class DemandForecast(BaseModel):
    id: str
    item_sku: str
    item_name: str
    current_demand: int
    forecasted_demand: int
    trend: str
    period: str

class BacklogItem(BaseModel):
    id: str
    order_id: str
    item_sku: str
    item_name: str
    quantity_needed: int
    quantity_available: int
    days_delayed: int
    priority: str
    has_purchase_order: Optional[bool] = False

class PurchaseOrder(BaseModel):
    id: str
    backlog_item_id: str
    supplier_name: str
    quantity: int
    unit_cost: float
    expected_delivery_date: str
    status: str
    created_date: str
    notes: Optional[str] = None

class CreatePurchaseOrderRequest(BaseModel):
    backlog_item_id: str
    supplier_name: str
    quantity: int
    unit_cost: float
    expected_delivery_date: str
    notes: Optional[str] = None

class QuarterlyReport(BaseModel):
    quarter: str
    total_orders: int
    total_revenue: float
    avg_order_value: float
    fulfillment_rate: float

class MonthlyTrend(BaseModel):
    month: str
    order_count: int
    revenue: float
    delivered_count: int

class Task(BaseModel):
    id: str
    title: str
    priority: str = 'medium'
    due_date: Optional[str] = None
    status: str = 'pending'

class CreateTaskRequest(BaseModel):
    title: str
    priority: str = 'medium'
    due_date: Optional[str] = None

class RestockingRecommendation(BaseModel):
    sku: str
    name: str
    category: str
    warehouse: str
    quantity_on_hand: int
    reorder_point: int
    recommended_quantity: int
    unit_cost: float
    estimated_cost: float
    urgency: str
    urgency_score: float
    rationale: str
    demand_trend: Optional[str] = None
    backlog_days_delayed: Optional[int] = None

class RestockingResponse(BaseModel):
    budget: float
    total_estimated_cost: float
    items_recommended: int
    recommendations: List[RestockingRecommendation]
    filters: dict

# In-memory task storage
_tasks: list = []
_task_counter = [0]

# API endpoints

def _compute_urgency_score(inv_item, demand, backlog):
    reorder_pt = inv_item.get("reorder_point", 0)
    if reorder_pt == 0:
        stock_score = 0.0
    elif demand:
        coverage = inv_item["quantity_on_hand"] / max(demand["forecasted_demand"], 1)
        stock_score = max(0.0, min(1.0, 1.0 - coverage))
    else:
        coverage = inv_item["quantity_on_hand"] / max(reorder_pt, 1)
        stock_score = max(0.0, min(1.0, 1.0 - coverage))

    if demand:
        trend = demand["trend"]
        if trend == "increasing":
            pct = (demand["forecasted_demand"] - demand["current_demand"]) / max(demand["current_demand"], 1)
            trend_score = 0.7 + 0.3 * min(pct, 1.0)
        elif trend == "stable":
            trend_score = 0.3
        else:
            trend_score = 0.0
    else:
        trend_score = 0.0

    backlog_score = 1.0 if backlog else 0.0
    base = 0.50 * stock_score + 0.35 * trend_score + 0.15 * backlog_score

    below = inv_item["quantity_on_hand"] < reorder_pt
    if below and demand and demand.get("trend") == "increasing":
        base = min(1.0, base * 1.35)

    return round(base, 4)


def _score_to_label(score):
    if score >= 0.7:
        return "critical"
    elif score >= 0.4:
        return "high"
    elif score >= 0.2:
        return "medium"
    return "low"


def _compute_recommended_quantity(inv_item, demand, backlog):
    if demand:
        target = math.ceil(demand["forecasted_demand"] * 1.20)
    else:
        target = math.ceil(inv_item["reorder_point"] * 1.20)
    qty = max(0, target - inv_item["quantity_on_hand"])
    if qty == 0 and backlog:
        qty = max(1, backlog["quantity_needed"] - backlog["quantity_available"])
    return qty


def _build_rationale(inv_item, demand, backlog):
    parts = []
    if inv_item["quantity_on_hand"] < inv_item["reorder_point"]:
        deficit = inv_item["reorder_point"] - inv_item["quantity_on_hand"]
        parts.append(f"Below reorder point by {deficit} units")
    else:
        parts.append("At or above reorder point")

    if demand:
        trend = demand["trend"]
        if trend == "increasing":
            pct = round(
                (demand["forecasted_demand"] - demand["current_demand"])
                / max(demand["current_demand"], 1) * 100
            )
            parts.append(f"demand increasing {pct}%")
        elif trend == "decreasing":
            parts.append("demand decreasing")
        else:
            parts.append("demand stable")
    else:
        parts.append("no demand forecast available")

    if backlog:
        parts.append(
            f"active backlog {backlog['days_delayed']} day(s) delayed ({backlog['priority']} priority)"
        )

    return "; ".join(parts)

# Restocking helper functions
@app.get("/")
def root():
    return {"message": "Factory Inventory Management System API", "version": "1.0.0"}

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(
    warehouse: Optional[str] = None,
    category: Optional[str] = None
):
    """Get all inventory items with optional filtering"""
    return apply_filters(inventory_items, warehouse, category)

@app.get("/api/inventory/{item_id}", response_model=InventoryItem)
def get_inventory_item(item_id: str):
    """Get a specific inventory item"""
    item = next((item for item in inventory_items if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/api/orders", response_model=List[Order])
def get_orders(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    month: Optional[str] = None
):
    """Get all orders with optional filtering"""
    filtered_orders = apply_filters(orders, warehouse, category, status)
    filtered_orders = filter_by_month(filtered_orders, month)
    return filtered_orders

@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    """Get a specific order"""
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/api/demand", response_model=List[DemandForecast])
def get_demand_forecasts():
    """Get demand forecasts"""
    return demand_forecasts

@app.get("/api/backlog", response_model=List[BacklogItem])
def get_backlog():
    """Get backlog items with purchase order status"""
    # Add has_purchase_order flag to each backlog item
    result = []
    for item in backlog_items:
        item_dict = dict(item)
        # Check if this backlog item has a purchase order
        has_po = any(po["backlog_item_id"] == item["id"] for po in purchase_orders)
        item_dict["has_purchase_order"] = has_po
        result.append(item_dict)
    return result

@app.get("/api/dashboard/summary")
def get_dashboard_summary(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    month: Optional[str] = None
):
    """Get summary statistics for dashboard with optional filtering"""
    # Filter inventory
    filtered_inventory = apply_filters(inventory_items, warehouse, category)

    # Filter orders
    filtered_orders = apply_filters(orders, warehouse, category, status)
    filtered_orders = filter_by_month(filtered_orders, month)

    total_inventory_value = sum(item["quantity_on_hand"] * item["unit_cost"] for item in filtered_inventory)
    low_stock_items = len([item for item in filtered_inventory if item["quantity_on_hand"] <= item["reorder_point"]])
    pending_orders = len([order for order in filtered_orders if order["status"] in ["Processing", "Backordered"]])
    total_backlog_items = len(backlog_items)

    return {
        "total_inventory_value": round(total_inventory_value, 2),
        "low_stock_items": low_stock_items,
        "pending_orders": pending_orders,
        "total_backlog_items": total_backlog_items,
        "total_orders_value": sum(order["total_value"] for order in filtered_orders)
    }

@app.get("/api/spending/summary")
def get_spending_summary():
    """Get spending summary statistics"""
    return spending_summary

@app.get("/api/spending/monthly")
def get_monthly_spending():
    """Get monthly spending breakdown"""
    return monthly_spending

@app.get("/api/spending/categories")
def get_category_spending():
    """Get spending by category"""
    return category_spending

@app.get("/api/spending/transactions")
def get_recent_transactions():
    """Get recent transactions"""
    return recent_transactions

@app.get("/api/reports/quarterly", response_model=List[QuarterlyReport])
def get_quarterly_reports(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    month: Optional[str] = None
):
    """Get quarterly performance reports"""
    # Calculate quarterly statistics from orders
    filtered_orders = apply_filters(orders, warehouse, category)
    filtered_orders = filter_by_month(filtered_orders, month)

    quarters = {}

    for order in filtered_orders:
        order_date = order.get('order_date', '')
        # Determine quarter
        if '2025-01' in order_date or '2025-02' in order_date or '2025-03' in order_date:
            quarter = 'Q1-2025'
        elif '2025-04' in order_date or '2025-05' in order_date or '2025-06' in order_date:
            quarter = 'Q2-2025'
        elif '2025-07' in order_date or '2025-08' in order_date or '2025-09' in order_date:
            quarter = 'Q3-2025'
        elif '2025-10' in order_date or '2025-11' in order_date or '2025-12' in order_date:
            quarter = 'Q4-2025'
        else:
            continue

        if quarter not in quarters:
            quarters[quarter] = {
                'quarter': quarter,
                'total_orders': 0,
                'total_revenue': 0,
                'delivered_orders': 0,
                'avg_order_value': 0
            }

        quarters[quarter]['total_orders'] += 1
        quarters[quarter]['total_revenue'] += order.get('total_value', 0)
        if order.get('status') == 'Delivered':
            quarters[quarter]['delivered_orders'] += 1

    # Calculate averages and fulfillment rate
    result = []
    for q, data in quarters.items():
        avg_order_value = 0.0
        fulfillment_rate = 0.0
        if data['total_orders'] > 0:
            avg_order_value = round(data['total_revenue'] / data['total_orders'], 2)
            fulfillment_rate = round((data['delivered_orders'] / data['total_orders']) * 100, 1)
        result.append({
            'quarter': data['quarter'],
            'total_orders': data['total_orders'],
            'total_revenue': data['total_revenue'],
            'avg_order_value': avg_order_value,
            'fulfillment_rate': fulfillment_rate,
        })

    # Sort by quarter
    result.sort(key=lambda x: x['quarter'])
    return result

@app.get("/api/reports/monthly-trends", response_model=List[MonthlyTrend])
def get_monthly_trends(
    warehouse: Optional[str] = None,
    category: Optional[str] = None,
    month: Optional[str] = None
):
    """Get month-over-month trends"""
    months = {}

    filtered_orders = apply_filters(orders, warehouse, category)
    filtered_orders = filter_by_month(filtered_orders, month)

    for order in filtered_orders:
        order_date = order.get('order_date', '')
        if not order_date:
            continue

        # Extract month (format: YYYY-MM-DD)
        order_month = order_date[:7]  # Gets YYYY-MM

        if order_month not in months:
            months[order_month] = {
                'month': order_month,
                'order_count': 0,
                'revenue': 0,
                'delivered_count': 0
            }

        months[order_month]['order_count'] += 1
        months[order_month]['revenue'] += order.get('total_value', 0)
        if order.get('status') == 'Delivered':
            months[order_month]['delivered_count'] += 1

    # Convert to list and sort
    result = list(months.values())
    result.sort(key=lambda x: x['month'])
    return result

@app.get("/api/restocking/recommendations", response_model=RestockingResponse)
def get_restocking_recommendations(
    budget: float = 0,
    warehouse: str = "all",
    category: str = "all",
):
    """Get restocking recommendations ranked by urgency with optional budget ceiling."""
    filtered_inv = apply_filters(inventory_items, warehouse, category)

    demand_by_sku = {d["item_sku"]: d for d in demand_forecasts}
    backlog_by_sku: dict = {}
    for b in backlog_items:
        sku = b["item_sku"]
        if sku not in backlog_by_sku or b["days_delayed"] > backlog_by_sku[sku]["days_delayed"]:
            backlog_by_sku[sku] = b

    candidates = []
    for item in filtered_inv:
        sku = item["sku"]
        demand = demand_by_sku.get(sku)
        backlog = backlog_by_sku.get(sku)

        below_reorder = item["quantity_on_hand"] < item["reorder_point"]
        has_backlog = backlog is not None

        if not below_reorder and not has_backlog:
            continue

        score = _compute_urgency_score(item, demand, backlog)
        label = _score_to_label(score)
        rec_qty = _compute_recommended_quantity(item, demand, backlog)
        est_cost = round(rec_qty * item["unit_cost"], 2)

        candidates.append({
            "sku": sku,
            "name": item["name"],
            "category": item["category"],
            "warehouse": item["warehouse"],
            "quantity_on_hand": item["quantity_on_hand"],
            "reorder_point": item["reorder_point"],
            "recommended_quantity": rec_qty,
            "unit_cost": item["unit_cost"],
            "estimated_cost": est_cost,
            "urgency": label,
            "urgency_score": score,
            "rationale": _build_rationale(item, demand, backlog),
            "demand_trend": demand["trend"] if demand else None,
            "backlog_days_delayed": backlog["days_delayed"] if backlog else None,
        })

    candidates.sort(key=lambda x: x["urgency_score"], reverse=True)

    if budget > 0:
        selected = []
        remaining = budget
        for item in candidates:
            if item["estimated_cost"] <= remaining:
                selected.append(item)
                remaining -= item["estimated_cost"]
        candidates = selected

    total_cost = round(sum(r["estimated_cost"] for r in candidates), 2)
    all_warehouses = sorted({item["warehouse"] for item in inventory_items})
    all_categories = sorted({item["category"] for item in inventory_items})

    return {
        "budget": budget,
        "total_estimated_cost": total_cost,
        "items_recommended": len(candidates),
        "recommendations": candidates,
        "filters": {
            "warehouses": all_warehouses,
            "categories": all_categories,
        },
    }

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    """Get all tasks"""
    return _tasks

@app.post("/api/tasks", response_model=Task)
def create_task(task: CreateTaskRequest):
    """Create a new task"""
    _task_counter[0] += 1
    new_task = {
        "id": f"api-{_task_counter[0]}",
        "title": task.title,
        "priority": task.priority,
        "due_date": task.due_date,
        "status": "pending"
    }
    _tasks.append(new_task)
    return new_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task"""
    task = next((t for t in _tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    _tasks.remove(task)
    return {"message": "Task deleted"}

@app.patch("/api/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: str):
    """Toggle task completion status"""
    task = next((t for t in _tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["status"] = "completed" if task["status"] == "pending" else "pending"
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
