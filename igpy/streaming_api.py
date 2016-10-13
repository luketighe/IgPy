from igpy.lightstreamer import LSClient,Subscription


class IGStreamingApi(object):

    def __init__(self, broker):
        self.broker = broker
        self.broker.login()
        self.ls_client = LSClient(broker.lightstreamer_endpoint, user=broker.identifier, password='CST-' + broker.cst_token + '|XST-' + broker.security_token)

        try:
            self.ls_client.connect()
        except Exception as e:
            print(e)

    def subscribe(self, mode, epics, fields, item_handler):

        subscription = Subscription(
            mode=mode,
            items=epics,
            fields=fields
        )

        subscription.addlistener(item_handler)
        sub_key = self.ls_client.subscribe(subscription)