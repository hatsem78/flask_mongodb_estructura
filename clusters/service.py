from flask import abort
from bson import ObjectId
from passlib.hash import sha256_crypt
from utils.db_utils import Base
from utils.helper import custom_marshal
from models import Cluster
import re

base_obj = Base()


class ClusterService(object):
    """
    Service Class for User View
    """

    def create(self, payload):
        """
        signup function
        :return:
        """

        try:
            if payload.get('cluster_name') == "":
                return {'msg': "Cluster name is requerid", 'code': 0}
            records = Cluster.objects(
                cluster_name__exact=payload.get('cluster_name'))

            #_id = base_obj.insert(COLLECTIONS['USERS'], payload)
            if records.count() > 0:
                return {'msg': 'Cluster Aready Exists', 'code': 0}

            cluster = Cluster(
                cluster_name=payload.get('cluster_name'),
                cluster_id=payload.get('cluster_id'),
            )

            _id = Cluster.objects.insert(cluster)

            return {'msg': _id.pk, 'code': 1}
        except Exception as err:
            print(err)
            return err

    def update(self, payload):
        try:
            cluster = Cluster.objects(_id=id).get()
            cluster.update(
                cluster_name=payload['cluster_name'],
            )

            return {'msg': "User updated!", 'code': 1}
        except Exception as err:
            print(err)
            return {'msg': "User not updated!", 'code': 0}
