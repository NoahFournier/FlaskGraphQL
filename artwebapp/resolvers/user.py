from artwebapp.entities.user import User

def resolve_users(obj, info):
    """Resolver function for 'users' Query"""
    try:
        users = [user.to_dict() for user in User.query.all()]
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [error]
        }
    return payload