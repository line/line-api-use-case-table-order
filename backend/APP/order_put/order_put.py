import logging
import json
import os
import uuid
import datetime
from decimal import Decimal
from dateutil.tz import gettz
from botocore.exceptions import ClientError
from common import (common_const, utils, line)

from validation.table_order_param_check import TableOrderParamCheck
from table_order.table_order_item_list import TableOrderItemList  # noqa501
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501


# 環境変数の取得
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
item_list_table_controller = TableOrderItemList()
payment_order_table_controller = TableOrderPaymentOrderInfo()

# 定数の定義
DISCOUNT_BY_PRICE = 1
DISCOUNT_BY_PERCENTAGE = 2


def create_payment_info(params, now):
    """
    新規の注文情報を登録する

    Parameters
    ----------
    params : dict
        postで送られてきたbodyの中身
    now : string
        現在時刻 [yyyy-m-d H:m:s]

    Returns
    -------
    payment_id:str
        新規発行したpaymentId
    """
    # DBより商品情報を取得し、登録用データを作成する
    put_order_items = get_order_item_info(params['item']) 
    payment_id = str(uuid.uuid4())
    payment_info = {
        'paymentId': payment_id,
        'userId': params['userId'],
        'transactionId': 0,
        'order': [
            {
                'orderId': 1,
                'item': put_order_items,
                'tableId': params['tableId'],
                'cancel': False,
                'deleteReason': '',
                'orderDateTime': now
            }
        ]
    }
    calc_amount(payment_info)
    try:
        payment_order_table_controller.put_item(payment_info)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.error("ID[%s]は重複しています。", payment_id)
            payment_info['paymentId'] = str(uuid.uuid4())
            payment_order_table_controller.put_item(
                payment_info)
        raise

    return payment_info['paymentId']


def calc_amount(payment_info):
    """
    合計金額を算出する
    Parameters
    ----------
    payment_info : dict
        新規に追加する注文情報
    Returns
    -------
    amount : Decimal
        合計金額
    """
    amount = 0
    for order in payment_info['order']:
        for item in order['item']:
            price = item['price']
            if item['discountWay'] == DISCOUNT_BY_PRICE:
                price = price - item['discountRate']
            elif item['discountWay'] == DISCOUNT_BY_PERCENTAGE:
                price = float(price) * (1 - float(item['discountRate']) * 0.01)
            amount = amount + float(price) * float(item['orderNum'])

    amount = Decimal(amount)
    payment_info['amount'] = amount
    return amount


def get_item_info_item_id(item_id, order_num, item_info_list):
    """
    itemIdをもとに商品情報を取得し、データを登録用に成形

    Parameters
    ----------
    item_id: string
        注文する商品ID
    order_num: int
        注文数量
    item_info_list : list
        １カテゴリの商品情報

    Returns
    -------
    order_item:dict
        注文商品情報
    """
    # masterデータをfor文にして注文itemIdと合致する場合、登録用データを作成する
    for master_item in item_info_list['items']:
        # マスタデータと注文データのitemIdが合致したらデータセット
        if master_item['itemId'] == item_id:
            order_item = {
                'itemId': master_item['itemId'],
                'itemName': master_item['itemName'],
                'orderNum': order_num,
                'price': master_item['price'],
                'discountRate': master_item['discountRate'],
                'discountWay': master_item['discountWay'],
                'imageUrl': master_item['imageUrl'],
                }
            return order_item


def get_order_item_info(item):
    """
    categoryIdとitemIdを元に注文登録用の商品情報を取得する

    Parameters
    ----------
    item : list
        postで送られてきたbodyの中身

    Returns
    -------
    put_order_items:dict
        注文商品情報
    """
    # カテゴリーID種類数だけDBに問い合わせるため、item内をカテゴリーIDで昇順にする
    order_items = sorted(item, key=lambda x: x['categoryId'])
    category_id = None
    item_info_list = []     # DBから取得したマスタデータ
    put_order_items = []    # DBに登録する商品リスト
    for item in order_items:
        if category_id is None:
            category_id = item['categoryId']
            item_info_list = item_list_table_controller.get_item(
                category_id)
        elif category_id != item['categoryId']:
            item_info_list = item_list_table_controller.get_item(
                item['categoryId'])
        put_order_items.append(
            get_item_info_item_id(
                item['itemId'], item['orderNum'], item_info_list))
    
    return put_order_items


def update_payment_info(params, now):
    """
    指定のpaymentIdの注文情報を更新する

    Parameters
    ----------
    params : dict
        postで送られてきたbodyの中身
    now : string
        現在時刻 [yyyy-m-d H:m:s] の形式

    Returns
    -------
    payment_id:int
        更新したドキュメントのpaymentId
    """
    # DBより商品情報を取得し、登録データを作成する
    put_order_items = get_order_item_info(params['item']) 
    payment_id = params['paymentId']
    payment_info = payment_order_table_controller.get_item(
        payment_id)

    order_id = len(payment_info['order']) + 1
    order = {
        'orderId': order_id,
        'item': put_order_items,
        'orderDateTime': now,
        'paymentDeleteFlg': False,
        'tableId': 5,
        'cancel': False,
        'deleteReason': ''
    }
    payment_info['order'].append(order)

    calc_amount(payment_info)

    logger.debug('modifiedItem %s', payment_info['order'])

    try:
        payment_order_table_controller.update_order(
            payment_id, params['userId'],
            payment_info['order'], payment_info['amount']
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.error("会計済みか、ユーザーIDが誤っています。[payment_id: %s, userId: %s]",
                         payment_id, params['userId'])
        raise

    return payment_id


def put_order(params):
    """
    商品情報一覧の取得

    Parameters
    ----------
    params : dict
        APIGatewayのGETパラメータ

    Returns
    -------
    paymentId:str
        paymentId(create_payment_infoのreturn値)
    """
    now = datetime.datetime.now(
        gettz('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')

    if 'paymentId' in params and params['paymentId']:
        return update_payment_info(params, now)

    return create_payment_info(params, now)


def lambda_handler(event, context):
    """
    注文情報を登録する
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容
    Returns
    -------
    payment_id : dict
        会計ID
    """
    # パラメータログ
    logger.info(event)
    if event['body'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    body = json.loads(event['body'])

    # ユーザーID取得
    try:
        user_profile = line.get_profile(body['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(body)

    if error_msg := param_checker.check_api_order_put():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    try:
        payment_id = put_order(body)
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')
    return utils.create_success_response(
        json.dumps(payment_id, default=utils.decimal_to_int,
                   ensure_ascii=False))
