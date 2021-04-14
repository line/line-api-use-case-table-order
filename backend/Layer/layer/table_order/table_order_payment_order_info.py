"""
TableOrderPaymentOrderInfo操作用モジュール

"""
import os
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB
from common import utils


class TableOrderPaymentOrderInfo(DynamoDB):
    """TableOrderPaymentOrderInfo操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("PAYMENT_ORDER_DB")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def get_item(self, payment_id):
        """
        データ取得

        Parameters
        ----------
        payment_id : int
            会計

        Returns
        -------
        item : dict
            注文情報

        """
        key = {'paymentId': payment_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def query_index_user_id_transaction_id(self, user_id, transaction_id):  # noqa: E501
        """
        queryメソッドを使用してstaffId-reservedYearMonth-indexのインデックスからデータ取得

        Parameters
        ----------
        user_id : str
            ユーザーID
        transaction_id : str
            LINE PayのtransactionID

        Returns
        -------
        items : list
            特定年月の予約情報のリスト

        """
        index = 'userId-index'
        expression = 'userId = :user_id AND transactionId = :transaction_id'  # noqa: E501
        expression_value = {
            ':user_id': user_id,
            ':transaction_id': transaction_id
        }

        try:
            items = self._query_index(index, expression, expression_value)
        except Exception as e:
            raise e
        return items

    def put_item(self, order_info):
        """
        データ登録

        Parameters
        ----------
        order_info:dict
            注文情報
        payment_id : int
            会計ID
        amount : int
            注文金額
        order : dict
            注文情報
        user_id : str
            ユーザーID

        Returns
        -------
        response :dict
            DB登録レスポンス情報

        """
        item = {
            "paymentId": order_info['paymentId'],
            "amount": order_info['amount'],
            "order": order_info['order'],
            "userId": order_info['userId'],
            "transactionId": 0,
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
        }
        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response

    def update_order(self, payment_id, user_id, order, amount):
        """
        データ更新

        Parameters
        ----------
        order_info:dict
            注文情報
        payment_id : int
            会計ID
        amount : int
            注文金額
        order : dict
            注文情報
        user_id : str
            ユーザーID

        Returns
        -------
        response :dict
            DB更新レスポンス情報

        """
        key = {'paymentId': payment_id}
        update_expression = ('set #od = :order, '
                             'amount = :amount, '
                             'updatedTime = :updatedTime')
        condition_expression = ('transactionId = :transactionId AND '
                                'userId = :uid')
        expression_attribute_names = {'#od': 'order'}
        expression_value = {
            ':order': order,
            ':amount': amount,
            ':uid': user_id,
            ':transactionId': 0,
            ':updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
        }
        return_value = "UPDATED_NEW"

        try:
            response = self._update_item_optional(
                key, update_expression, condition_expression,
                expression_attribute_names, expression_value, return_value)
        except Exception as e:
            raise e
        return response

    def update_payment_info(self, payment_id, transaction_id):
        """
        データ更新

        Parameters
        ----------
        payment_id:int
            会計ID
        transaction_id : str
            LINE PayのtransactionId

        Returns
        -------
        response :dict
            DB更新レスポンス情報

        """
        key = {'paymentId': payment_id}
        update_expression = ('set transactionId = :transactionId, '
                             'paidDatetime = :paidDatetime, '
                             'expirationDate = :expirationDate, '
                             'updatedTime = :updatedTime')
        now = datetime.now(gettz('Asia/Tokyo'))
        datetime_now = str(now)
        expression_value = {
            ':transactionId': transaction_id,
            ':expirationDate': utils.get_ttl_time(now),
            ':paidDatetime': datetime_now,
            ':updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
        }
        return_value = "UPDATED_NEW"

        try:
            response = self._update_item(
                key, update_expression, expression_value, return_value)
        except Exception as e:
            raise e
        return response
