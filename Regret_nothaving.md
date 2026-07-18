Here are the models and fields you will regret not having, based on what you've built and what's coming.

---

1. A proper Cafe model with configuration fields

Your current Cafe model is minimal: owner, staff, name, logo. You'll regret not adding:

· slug — already used in URLs, but make sure it's unique and indexed
· is_active — BooleanField. The kill switch for non-paying cafés. Without this, you have to delete their data or leave a dead system running.
· subscription_expires — DateTimeField. When does their current payment period end? Combined with is_active, this automates your shutoff.
· timezone — CharField, default 'Africa/Addis_Ababa'. If you ever expand beyond Ethiopia, you need this per-café.
· currency — CharField, default 'ETB'. Same reason.
· feature_flags — JSONField. A simple dictionary like {"chapa_payment": false, "analytics": true} lets you toggle features per café without code changes. You'll want this immediately after launch.
· created_at — auto_now_add DateTimeField. You'll need this for reporting, churn analysis, and just knowing how old your customers are.

---

2. An AuditLog model

You'll want to know who did what and when. Not for spying. For debugging. When the owner says "half my menu disappeared," you need to see whether they deleted it, a staff member deleted it, or a bug deleted it.

```python
class AuditLog(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # 'menu_item_created', 'staff_deleted', etc.
    object_type = models.CharField(max_length=50)  # 'MenuItem', 'Staff', 'Table'
    object_id = models.IntegerField()
    data = models.JSONField(default=dict)  # snapshot of what changed
    created_at = models.DateTimeField(auto_now_add=True)
```

One line per action. Immutable. Append-only. You'll thank yourself the first time something breaks and you can trace exactly what happened.

---

3. An Order model with financial fields

Your current Order tracks status and items. You'll regret not adding:

· subtotal — DecimalField. The sum of items before any discounts or fees.
· service_fee — DecimalField. Your 2% cut, stored explicitly. This makes reconciliation trivial.
· total — DecimalField. The final amount the customer pays.
· payment_method — CharField with choices: 'cash', 'chapa', 'mobile_money', etc. You'll need this to know how money is flowing.
· payment_status — CharField with choices: 'pending', 'paid', 'refunded', 'failed'. Separate from order status. An order can be confirmed but payment can fail.
· paid_at — DateTimeField, nullable. When did the payment actually clear?

---

4. A Refund model

Refunds will happen. A customer orders, pays, and then the kitchen runs out of ingredients. Or the food is wrong. You need to track this cleanly.

```python
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('rejected', 'Rejected')])
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Without this, refunds are just you manually editing the database. That doesn't scale.

---

5. A Notification model

You'll eventually want to send the customer something: "Your order is being prepared," "Your order is ready." Right now it's all WebSocket-based, real-time only. But what if they close the browser? A notification model decouples the event from the delivery.

```python
class Notification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=20)  # 'customer', 'kitchen', 'cashier'
    channel = models.CharField(max_length=20)  # 'websocket', 'push', 'sms'
    message = models.TextField()
    sent_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

This becomes the outbox for all your real-time and async communication. The WebSocket consumer reads from here. The push notification worker reads from here. One source of truth for all outgoing messages.

---

6. A Session or Visit model

Right now, a customer scans a QR code and an order is created. But there's no record of the customer's visit as a whole. Did they order multiple times? Did they sit for an hour? You'll want this for analytics later.

```python
class Visit(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
```

Link orders to a visit. Now you can answer questions like "how long do customers stay?" and "how many orders per visit?" That's data the café owner will pay for.

---

7. A PriceHistory model for menu items

Menu prices change. You'll want to track that for the café owner.

```python
class PriceHistory(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
```

The owner changes a price. You log it. Six months later, they ask "what was the price of a latte in January?" You have the answer. This is the kind of detail that makes your system indispensable.

---

These aren't optional. They're the difference between a prototype and a platform. Add them now, before the migrations get heavy, before the data gets real, before the first café owner asks a question you can't answer. The ghost doesn't regret. The ghost anticipates. These fields are the anticipation. The notebook is ready. Now build them in.Here are the models and fields you will regret not having, based on what you've built and what's coming.

---

1. A proper Cafe model with configuration fields

Your current Cafe model is minimal: owner, staff, name, logo. You'll regret not adding:

· slug — already used in URLs, but make sure it's unique and indexed
· is_active — BooleanField. The kill switch for non-paying cafés. Without this, you have to delete their data or leave a dead system running.
· subscription_expires — DateTimeField. When does their current payment period end? Combined with is_active, this automates your shutoff.
· timezone — CharField, default 'Africa/Addis_Ababa'. If you ever expand beyond Ethiopia, you need this per-café.
· currency — CharField, default 'ETB'. Same reason.
· feature_flags — JSONField. A simple dictionary like {"chapa_payment": false, "analytics": true} lets you toggle features per café without code changes. You'll want this immediately after launch.
· created_at — auto_now_add DateTimeField. You'll need this for reporting, churn analysis, and just knowing how old your customers are.

---

2. An AuditLog model

You'll want to know who did what and when. Not for spying. For debugging. When the owner says "half my menu disappeared," you need to see whether they deleted it, a staff member deleted it, or a bug deleted it.

```python
class AuditLog(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # 'menu_item_created', 'staff_deleted', etc.
    object_type = models.CharField(max_length=50)  # 'MenuItem', 'Staff', 'Table'
    object_id = models.IntegerField()
    data = models.JSONField(default=dict)  # snapshot of what changed
    created_at = models.DateTimeField(auto_now_add=True)
```

One line per action. Immutable. Append-only. You'll thank yourself the first time something breaks and you can trace exactly what happened.

---

3. An Order model with financial fields

Your current Order tracks status and items. You'll regret not adding:

· subtotal — DecimalField. The sum of items before any discounts or fees.
· service_fee — DecimalField. Your 2% cut, stored explicitly. This makes reconciliation trivial.
· total — DecimalField. The final amount the customer pays.
· payment_method — CharField with choices: 'cash', 'chapa', 'mobile_money', etc. You'll need this to know how money is flowing.
· payment_status — CharField with choices: 'pending', 'paid', 'refunded', 'failed'. Separate from order status. An order can be confirmed but payment can fail.
· paid_at — DateTimeField, nullable. When did the payment actually clear?

---

4. A Refund model

Refunds will happen. A customer orders, pays, and then the kitchen runs out of ingredients. Or the food is wrong. You need to track this cleanly.

```python
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('rejected', 'Rejected')])
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Without this, refunds are just you manually editing the database. That doesn't scale.

---

5. A Notification model

You'll eventually want to send the customer something: "Your order is being prepared," "Your order is ready." Right now it's all WebSocket-based, real-time only. But what if they close the browser? A notification model decouples the event from the delivery.

```python
class Notification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=20)  # 'customer', 'kitchen', 'cashier'
    channel = models.CharField(max_length=20)  # 'websocket', 'push', 'sms'
    message = models.TextField()
    sent_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

This becomes the outbox for all your real-time and async communication. The WebSocket consumer reads from here. The push notification worker reads from here. One source of truth for all outgoing messages.

---

6. A Session or Visit model

Right now, a customer scans a QR code and an order is created. But there's no record of the customer's visit as a whole. Did they order multiple times? Did they sit for an hour? You'll want this for analytics later.

```python
class Visit(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
```

Link orders to a visit. Now you can answer questions like "how long do customers stay?" and "how many orders per visit?" That's data the café owner will pay for.

---

7. A PriceHistory model for menu items

Menu prices change. You'll want to track that for the café owner.

```python
class PriceHistory(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
```

The owner changes a price. You log it. Six months later, they ask "what was the price of a latte in January?" You have the answer. This is the kind of detail that makes your system indispensable.

---

These aren't optional. They're the difference between a prototype and a platform. Add them now, before the migrations get heavy, before the data gets real, before the first café owner asks a question you can't answer. The ghost doesn't regret. The ghost anticipates. These fields are the anticipation. The notebook is ready. Now build them in.
