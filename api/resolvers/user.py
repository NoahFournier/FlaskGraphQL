from api.entities.user import User

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

def resolve_user(obj, info, user_id):
    """Resolver function for 'user' Query"""
    try:
        user = User.get_by_id(user_id).to_dict()
        print(user)
        payload = {
            "success": True,
            "users": [user]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [error]
        }
    return payload