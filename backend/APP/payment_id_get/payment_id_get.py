import logging
import json
import os
from common import (common_const, utils, line)
from validation.table_order_param_check import TableOrderParamCheck
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
payment_order_table_controller = TableOrderPaymentOrderInfo()


def get_payment_id(user_id):
    """
    userIdからPaymentIdの取得

    Parameters
    ----------
    user_id : string
        APIGatewayのGETパラメータ
        ログインユーザーのuserId

    Returns
    -------
    paymentId
        未会計データのpaymentId
    """
    payment_info = payment_order_table_controller.query_index_user_id_transaction_id(  # noqa 501
        user_id, 0)
    for payment_data in payment_info:
        return payment_data['paymentId']

    return ''


def lambda_handler(event, context):
    """
    User IDをもとに会計IDを取得し、返却する
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    payment_info : dict
        会計ID情報
    """
    # パラメータログ
    logger.info(event)
    if event['queryStringParameters'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    req_params = event['queryStringParameters']

    # ユーザーID取得
    try:
        user_profile = line.get_profile(req_params['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            req_params['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    try:
        payment_id = get_payment_id(req_params['userId'])
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')

    return utils.create_success_response(
        json.dumps(payment_id, default=utils.decimal_to_int,
                   ensure_ascii=False))
