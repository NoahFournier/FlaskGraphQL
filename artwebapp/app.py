import logging
import sys
from ariadne import snake_case_fallback_resolvers, make_executable_schema, load_schema_from_path, gql, graphql_sync, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from artwebapp.extensions import (
    db,
    migrate,
    debug_toolbar,
    login_manager,
    bcrypt,
    cache
)
from artwebapp import commands, entities
from artwebapp.resolvers.user import resolve_users

def create_app(config_object="artwebapp.settings"):
    """Create application factory

    :param config_object: The configuration object to use
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_routes(app)
    register_shellcontext(app)
    register_commands(app)
    register_graphql(app)
    return app

def register_extensions(app):
    """Register Flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    debug_toolbar.init_app(app)
    return None

def register_routes(app):
    """Register app routes"""
    @app.route('/')
    def hello_world():
        return 'Hello, World'
    
def register_commands(app):
    """Register Click commands"""
    app.cli.add_command(commands.test)

def register_shellcontext(app):
    """Register shell context objects"""

    def shell_context():
        """Shell context objects"""
        return {"db": db, "User": entities.user.User}
    
    app.shell_context_processor(shell_context)

def register_graphql(app):
    """Register GraphQL API & Playground route"""

    query = ObjectType("Query")

    query.set_field("users", resolve_users)

    type_defs = gql(load_schema_from_path("schema.graphql"))
    schema = make_executable_schema(
        type_defs, query, snake_case_fallback_resolvers
    )

    @app.route("/graphql", methods=["GET", "POST"])
    def graphql_playground():
        if request.method == "POST":
            data = request.get_json()
            success, result = graphql_sync(
                schema,
                data,
                context_value=request,
                debug=app.debug
            )
            status_code = 200 if success else 400
            return jsonify(result), status_code

        return PLAYGROUND_HTML, 200


