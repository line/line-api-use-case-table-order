"""
TableOrderItemList操作用モジュール

"""
import os
from aws.dynamodb.base import DynamoDB


class TableOrderItemList(DynamoDB):  # ()内のクラスを継承する
    """TableOrderItemList操作用クラス"""
    __slots__ = ['_table']  # インスタンス側で定義されたメンバ以外のメンバは持てなくなる

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("ITEM_LIST_DB")
        super().__init__(table_name)
        # 基底クラスのメソッドを使って初期化：テーブル名のセットとdynamodbリソースの生成
        self._table = self._db.Table(table_name)

    def get_item(self, category_id):
        """
        データ取得

        Parameters
        ----------
        category_id : int
            カテゴリーID

        Returns
        -------
        item : dict
            商品情報

        """
        key = {'categoryId': category_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def scan(self):
        """
        scanメソッドを使用してデータ取得

        Parameters
        ----------
        なし

        Returns
        -------
        items : list
            商品情報のリスト

        """
        key = 'category_id'

        try:
            items = self._scan(key)
        except Exception as e:
            raise e
        return items
