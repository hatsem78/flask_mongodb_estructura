from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from common.models import auth_parser
from models import Usuarios
from users_compesar.service import UsersCompensarService
from utils.decorator import token_required


users_compensar = Namespace(
    'Api user', description="Operaciones sobre usuarios")
users_compensar_service = UsersCompensarService()


@users_compensar.expect(auth_parser)
@users_compensar.route('/<string:id>/<string:id_type>')
class UsersCompensar(Resource):
    """
    Tasks Operations - Pass task room id as input
    """

    @token_required
    @jwt_required
    def get(self, id, id_type):
        """
        Active or Inactive User
        :param id:
        :return:
        """
        try:
            record = users_compensar_service.get_user_compensar(id, id_type)

            if 'estado_vinculacion' not in record:
                return {'status': 0, 'description': "User Not Activated", 'status_code': 200}
            else:

                record['Cluster'][0].pop("_id")
                record["Cluster"][0]["cluster"] = record["Cluster"][0].pop(
                    "cluster_name")
                record["Cluster"][0]["id_cluster"] = record["Cluster"][0].pop(
                    "cluster_id")

                return {
                    'status': 1,
                    'code': 'ok',
                    'message': {
                        'id_type': record['tipo_id_usurio'],
                        'cluster': record['Cluster'],
                        'id_worker': record['id_trabajador'],
                        'id': record['tipo_id_usurio'] + str(record['_id']),
                        'type': record['tipo_afilacion_trabajador'],
                        'id_type_worker': record['tipo_id_trabajador'],
                        'usos': record['Usos']
                    },

                    # 'status_code': 200
                }

        except Exception as err:
            print(err)
            return err

    @staticmethod
    def validate_usuario(state):
        if state == 'active' or state == 'archived' or state == 'deleted':
            return True
        else:
            return False
