from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}}, supports_credentials=True)

    # Register API blueprints
    from app.api.health import health_bp
    from app.api.auth import auth_bp
    from app.api.documents import documents_bp
    from app.api.analysis import analysis_bp
    from app.api.chat import chat_bp
    from app.api.audit import audit_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(documents_bp, url_prefix="/api")
    app.register_blueprint(analysis_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(audit_bp, url_prefix="/api")

    # Global JSON error handling for API routes
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        from flask import jsonify
        return jsonify({"error": "Database connection reset. Please retry your request."}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        import logging
        from flask import jsonify, request
        logging.getLogger(__name__).error(f"Unhandled exception on {request.path}: {error}", exc_info=True)
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({"error": "Server error. Please retry in a few moments."}), 500

    return app
