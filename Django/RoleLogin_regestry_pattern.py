class LoginRouter:
    _routes = {}
    
    @classmethod
    def register(cls, role):
        """Decorator that maps roles to their destinations"""
        def decorator(func):
            cls._routes[role] = func
            return func
        return decorator
    
    @classmethod
    def redirect(cls, role, user):
        """Route user to the correct page"""
        handler = cls._routes.get(role)
        if not handler:
            raise ValueError(f"No route defined for role: {role}")
        return handler(user)

# Each route is a standalone function—lives wherever it makes sense
@LoginRouter.register("admin")
def admin_dashboard(user):
    return f"Welcome Admin {user.name}, here's your dashboard with: system health, user management, billing"

@LoginRouter.register("manager")  
def manager_dashboard(user):
    return f"Welcome Manager {user.name}, here's your team dashboard with: team metrics, approvals, schedules"

@LoginRouter.register("employee")
def employee_dashboard(user):
    return f"Welcome {user.name}, here's your tasks and announcements"

# The login function becomes dead simple
def handle_login(username, password):
    user = authenticate(username, password)  # Your auth logic
    if not user:
        return "Invalid credentials"
    
    # One line. No if/elif. No switch.
    return LoginRouter.redirect(user.role, user)
