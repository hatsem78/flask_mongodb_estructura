from common.resources import *
from apiv1.auth import authapi
from users_compesar.views import users_compensar
from users.views import users_ns
from clusters.views import cluster_ns


#api.add_namespace(users_compensar, '/api/v1/usuario/activo')
api.add_namespace(authapi, '/api/apiv1')
api.add_namespace(users_ns, '/api/users')
api.add_namespace(cluster_ns, '/api/clusters')
api.add_namespace(users_compensar, '/api/usuarios')


if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get(
        'ENV') == 'development'  # Debug mode if development env
    app.run(host='0.0.0.0', port=600)  # Run the app
