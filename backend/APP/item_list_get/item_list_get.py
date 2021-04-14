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

# テーブル操作クラスの初期化
item_master_table_controller = TableOrderItemList()


def get_item_list(params):
    """
    指定のカテゴリの商品情報一覧を取得する

    Parameters
    ----------
    params : dict
        APIGatewayのGETパラメータ

    Returns
    -------
    items:dict
        商品情報一覧
    """

    category_id = 1
    if 'categoryId' in params and params['categoryId']:
        category_id = int(params['categoryId'])

    items = item_master_table_controller.get_item(category_id)
    logger.debug('items %s', items)
    return items


def lambda_handler(event, context):
    """
    商品情報を返す
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容
    Returns
    -------
    items : dict
        商品情報
    """
    # パラメータログ
    logger.info(event)

    try:
        items = get_item_list(event['queryStringParameters'])
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')

    return utils.create_success_response(
        json.dumps(items, default=utils.decimal_to_int,
                   ensure_ascii=False))
