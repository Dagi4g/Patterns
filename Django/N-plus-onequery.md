
# N+1 Query Problem

## Problem
When rendering a list with related objects in Django templates, the ORM can generate a separate database query for every row. If you display 50 orders, each with items, each item with a menu item, Django makes 1 query for orders, 50 queries for items, and potentially hundreds more for menu items. This kills performance at scale.

## Solution
Use `select_related` for ForeignKey relationships (one additional query via JOIN) and `prefetch_related` for reverse ForeignKey and ManyToMany relationships (one additional query per relationship, executed in Python).

## Snippet

```python
# Before: N+1 disaster
orders = Order.objects.filter(cafe=cafe)

# After: 3 queries total, regardless of result count
orders = Order.objects.filter(cafe=cafe)\
    .select_related('table', 'cashier')\
    .prefetch_related('items__menu_item')

```
