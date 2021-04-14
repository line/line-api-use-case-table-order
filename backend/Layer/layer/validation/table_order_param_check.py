from validation.param_check import ParamCheck


class TableOrderParamCheck(ParamCheck):
    def __init__(self, params):
        self.category_id = params['categoryId'] if 'categoryId' in params else None  # noqa:E501
        self.table_id = params['tableId'] if 'tableId' in params else None
        self.payment_id = params['paymentId'] if 'paymentId' in params else None  # noqa:E501
        self.transaction_id = params['transactionId'] if 'transactionId' in params else None  # noqa:E501

        self.item = params['item'] if 'item' in params else None  # noqa:E501

        self.error_msg = []

    def check_api_order_put(self):
        self.check_table_id()

        self.check_item()

        return self.error_msg

    def check_api_order_info(self):
        self.check_payment_id()

        return self.error_msg

    def check_api_payment_reserve(self):
        self.check_payment_id()

        return self.error_msg

    def check_api_payment_confirm(self):
        self.check_transaction_id()
        self.check_payment_id()

        return self.error_msg

    def check_api_payment_confirm_nolinepay(self):
        self.check_payment_id()

        return self.error_msg

    def check_table_id(self):
        if error := self.check_required(self.table_id, 'tableId'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.table_id, 'tableId', 1, None):
            self.error_msg.append(error)

    def check_category_id(self):
        if error := self.check_required(self.category_id, 'categoryId'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.category_id, 'categoryId', 1, None):  # noqa:E501
            self.error_msg.append(error)

    def check_payment_id(self):
        if error := self.check_required(self.payment_id, 'paymentId'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.payment_id, 'paymentId', 1, None):  # noqa:E501
            self.error_msg.append(error)

    def check_transaction_id(self):
        if error := self.check_required(self.transaction_id, 'transactionId'):
            self.error_msg.append(error)
            return

        if error := self.check_length(self.transaction_id, 'transactionId', 1, None):  # noqa:E501
            self.error_msg.append(error)

    def check_item(self):
        def check_category_id(self, category_id):
            if error := self.check_required(category_id, 'categoryId'):
                self.error_msg.append(error)
                return

        def check_item_id(self, item_id):
            if error := self.check_required(item_id, 'itemId'):
                self.error_msg.append(error)
                return

            if error := self.check_length(item_id, 'itemId', 1, None):  # noqa:E501
                self.error_msg.append(error)

        def check_order_num(self, order_num):
            if error := self.check_required(order_num, 'orderNum'):
                self.error_msg.append(error)
                return

        # itemがあるか確認→ない場合は中身のチェック無し
        if error := self.check_required(self.item, 'item'):
            self.error_msg.append(error)
            return

        # itemの中身をループでチェック
        for item_single in self.item:
            check_category_id(self,
                            item_single['categoryId']
                            if 'categoryId' in item_single else None)
            check_item_id(self,
                          item_single['itemId']
                          if 'itemId' in item_single else None)
            check_order_num(self,
                            item_single['orderNum']
                            if 'orderNum' in item_single else None)
