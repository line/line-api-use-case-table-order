import json
import os
import logging

from linepay import LinePayApi
from common import (common_const, utils, line)
from validation.table_order_param_check import TableOrderParamCheck
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501


# 環境変数
CONFIRM_URL = os.environ.get("CONFIRM_URL")
CANCEL_URL = os.environ.get("CANCEL_URL")
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)
# LINE Pay API情報
LINE_PAY_CHANNEL_ID = os.environ.get("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = os.environ.get("LINE_PAY_CHANNEL_SECRET")
if (os.environ.get("LINE_PAY_IS_SANDBOX") == 'True'
    or os.environ.get("LINE_PAY_IS_SANDBOX") == 'true'): 
    LINE_PAY_IS_SANDBOX = True
else:
    LINE_PAY_IS_SANDBOX = False
api = LinePayApi(LINE_PAY_CHANNEL_ID,
                 LINE_PAY_CHANNEL_SECRET, is_sandbox=LINE_PAY_IS_SANDBOX)
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# テーブル操作クラスの初期化
payment_order_table_controller = TableOrderPaymentOrderInfo()


def lambda_handler(event, context):
    """
    LINE Pay API(reserve)の通信結果を返す
    Parameters
    ----------
    event : dict
        POST時に渡されたパラメータ
    context : dict
        コンテキスト内容
    Returns
    -------
    response : dict
        LINE Pay APIの通信結果
    """

    logger.info(event)
    if event['body'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    req_body = json.loads(event['body'])

    # ユーザーID取得
    try:
        user_profile = line.get_profile(req_body['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            req_body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(req_body)

    if error_msg := param_checker.check_api_payment_reserve():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    payment_id = req_body['paymentId']
    payment_info = payment_order_table_controller.get_item(payment_id)
    amount = int(payment_info['amount'])
    body = {
        'amount': amount,
        'currency': 'JPY',
        'orderId': payment_id,
        'packages': [{
            'id': '1',
            'amount': amount,
            'name': 'LINE Use Case Barger',
            'products': [{
                'name': 'オーダー商品',
                'imageUrl': 'https://media.istockphoto.com/vectors/cash-register-with-a-paper-check-flat-isolated-vector-id1018485968',  # noqa:E501
                'quantity': '1',
                'price': amount
            }
            ]
        }],
        'redirectUrls': {
            'confirmUrl': CONFIRM_URL,
            'cancelUrl': CANCEL_URL
        },
        'options': {
            'payment': {
                'capture': 'True'
            }
        }
    }

    try:
        linepay_api_response = api.request(body)
        # 返却データ
        res_body = json.dumps(linepay_api_response)
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response("Error")
    else:
        return utils.create_success_response(res_body)
