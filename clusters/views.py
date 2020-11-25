from flask import request
from flask_restplus import Namespace, Resource, marshal
from clusters.models import cluster_base
from clusters.service import ClusterService
from run import api
from common.models import auth_parser
from utils.decorator import token_required, admin_token_required

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required,
    get_jti, get_raw_jwt, jwt_required)

from utils.decorator import token_required

jwt = JWTManager()

cluster_ns = Namespace('claster', description='Cluster Management')
cluster_service = ClusterService()


@cluster_ns.expect(auth_parser)
@cluster_ns.route('/create')
class Claster(Resource):
    '''
        Add claster
    '''
    @token_required
    @jwt_required
    @admin_token_required
    @cluster_ns.expect(cluster_base)
    def post(self):
        """
        Create Cluster use api
        :return:
        """
        payload = marshal(api.payload, cluster_base)

        record = cluster_service.create(payload)
        if record['code'] == 0:
            return {'status': 0, 'description': record['msg'], 'status_code': 400}
        else:
            return {'status': 1, 'description': "claster create Successfully", 'status_code': 200}


@cluster_ns.expect(auth_parser)
@cluster_ns.route('/update/<string:id>')
class ClasterUpdate(Resource):
    '''
        Update claster
    '''
    @token_required
    @jwt_required
    @admin_token_required
    @cluster_ns.expect(cluster_base)
    def post(self):
        """
            Update Cluster use api
            :param id:
            :return:
        """
        payload = marshal(api.payload, cluster_base)

        record = cluster_service.update(payload)
        if record['code'] == 0:
            return {'status': 0, 'description': record['msg'], 'status_code': 400}
        else:
            return {'status': 1, 'description': "claster create Successfully", 'id': record['msg'], 'status_code': 200}
