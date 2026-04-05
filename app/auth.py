def check_permission(role, action):
    if role == "admin":
        return True
    if role == "analyst" and action in ["view", "analyze"]:
        return True
    if role == "viewer" and action == "view":
        return True
    return False