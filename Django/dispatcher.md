# Single-Entry-Point Dispatcher Pattern

## Problem
When an app has many views that all require the same authentication and authorization (e.g., all owner views require `@owner_required`), repeating the decorator on every function is tedious and error-prone. Forgetting one decorator leaves a security hole.

## Solution
Route all same-role views through a single dispatcher function. The decorator fires once. The dispatcher calls the appropriate handler based on an `action` parameter.

## Snippet

```python
# views.py
from django.http import Http404
from owner.decorators import owner_required
from owner.models import Cafe

@owner_required
def owner_dispatcher(request, cafe_slug, action):
    """
    Single entry point for all owner views.
    Guaranteed: user is authenticated and has Owner role.
    """
    cafe = get_object_or_404(Cafe, slug=cafe_slug, owner=request.user)
    
    dispatcher = {
        'dashboard': owner_dashboard,
        'menu_list': menu_list,
        'menu_create': menu_create,
        'menu_edit': menu_edit,
        'menu_delete': menu_delete,
        'staff_list': staff_list,
        'staff_create': staff_create,
        'staff_edit': staff_edit,
        'staff_delete': staff_delete,
        'table_list': table_list,
        'table_enable': table_enable,
        'metrics': metrics,
    }
    
    handler = dispatcher.get(action)
    if handler is None:
        raise Http404(f"No owner action '{action}'")
    
    return handler(request, cafe_slug)


# Individual views: NO decorators, NO role checks, NO cafe fetching.
def owner_dashboard(request, cafe_slug):
    cafe = request.user.owned_cafes.get(slug=cafe_slug)
    menu_items = Menu.objects.filter(cafe=cafe)
    return render(request, 'owner/dashboard.html', {
        'cafe': cafe,
        'menu_items': menu_items,
    })

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:cafe_slug>/', views.owner_dispatcher, {'action': 'dashboard'}, name='owner-dashboard'),
    path('<slug:cafe_slug>/menu/', views.owner_dispatcher, {'action': 'menu_list'}, name='owner-menu-list'),
    path('<slug:cafe_slug>/menu/create/', views.owner_dispatcher, {'action': 'menu_create'}, name='owner-menu-create'),
    # ... all other owner URLs follow the same pattern
]

```
