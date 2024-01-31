from app.main import app


def reverse(endpoint_name: str, **kwargs) -> str:
    return app.url_path_for(endpoint_name, **kwargs)
