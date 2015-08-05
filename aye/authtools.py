from flask import g


def authenticate_user(user_id=None, auth_token_sent=None):
    """Boolean: User is authenticated in our system or not"""
    # If either of these is None, not authenticated
    if not user_id or not auth_token_sent:
        return False

    # Pull auth_token from db. This should be an in-memory store.
    # TODO: Switch to in-memory if performance drops
    cur = g.db_conn.cursor()
    cur.execute("SELECT current_auth_token from users \
                 WHERE fb_user_id = %(distance)s", user_id)

    db_response_map = cur.fetchone()
    if not db_response_map:
        return False

    curr_auth_token = db_response_map['current_auth_token']

    return (curr_auth_token is auth_token_sent)
