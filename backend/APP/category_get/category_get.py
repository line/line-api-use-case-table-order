import logging
import json
import os
from common import utils
from table_order.table_order_item_list import TableOrderItemList
# 環境変数の取得
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
item_master_table_controller = TableOrderItemList()


def get_category():
    """
    カテゴリIDとカテゴリ名を返却する

    Returns
    -------
    categories:dict
        商品カテゴリ一覧情報
    """

    categories = item_master_table_controller.scan()
    for category in categories:
        category.pop('items')
    return categories


def lambda_handler(event, context):
    """
    商品カテゴリ情報を返す
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    categories : dict
        商品カテゴリ一覧情報
    """
    # パラメータログ
    logger.info(event)
    try:
        categories = get_category()
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')

    return utils.create_success_response(
        json.dumps(categories, default=utils.decimal_to_int,
                   ensure_ascii=False))
