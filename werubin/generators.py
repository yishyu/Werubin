from drf_yasg.generators import OpenAPISchemaGenerator


# https://stackoverflow.com/questions/55568431/how-can-i-configure-https-schemes-with-the-drf-yasg-auto-generated-swagger-pag
class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema
