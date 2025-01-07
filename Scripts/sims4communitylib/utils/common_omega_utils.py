from distributor.ops import Op
from protocolbuffers.Consts_pb2 import MGR_UNMANAGED, MSG_OBJECTS_VIEW_UPDATE
from protocolbuffers.DistributorOps_pb2 import Operation
from protocolbuffers.Distributor_pb2 import ViewUpdate
from server.client import Client
from sims4communitylib.utils.misc.common_game_client_utils import CommonGameClientUtils


class CommonOmegaUtils:
    """ Utilities for sending messages to the client via the Omega channel. (Improved S4MP compatibility)

    Messages sent through this channel don't replicate to the rest of the clients in a multiplayer S4MP session.
    """

    @classmethod
    def send_view_update_message(cls, op: Op, manager_id=MGR_UNMANAGED, object_id=0, client: Client = None):
        import omega
        if client is None:
            client = CommonGameClientUtils.get_first_game_client()

        view_update = ViewUpdate()
        op_entry = view_update.entries.add()

        op_entry.primary_channel.id.manager_id = manager_id
        op_entry.primary_channel.id.object_id = object_id

        proto_buff = Operation()

        op.write(proto_buff)

        op_entry.operation_list.operations.append(proto_buff)
        omega.send(client.id, MSG_OBJECTS_VIEW_UPDATE, view_update.SerializeToString())
