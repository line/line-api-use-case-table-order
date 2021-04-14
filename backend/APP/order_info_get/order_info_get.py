import logging
import json
import os

from common import (common_const, utils)
from validation.table_order_param_check import TableOrderParamCheck
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501


# 環境変数の取得
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# テーブル操作クラスの初期化
payment_order_table_controller = TableOrderPaymentOrderInfo()


def get_order_info(params):
    """
    指定のpaymentIdの注文情報を取得する

    Parameters
    ----------
    params : dict
        APIGatewayのPOSTパラメータ
        paymentIdが渡される

    Returns
    -------
    payment_info:dict
        注文情報
    """

    payment_id = params['paymentId']
    payment_info = payment_order_table_controller.get_item(payment_id)
    logger.info(payment_info)
    if 'transactionId' in payment_info and payment_info['transactionId'] != 0:
        logger.error("[payment_id: %s] は会計済みの注文です。", payment_id)
        raise Exception

    return payment_info


def lambda_handler(event, context):
    """
    会計IDをもとに注文情報を取得し、返却する
    Parameters
    ----------
    event : dict
        フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    payment_info : dict
        注文情報
    """
    # パラメータログ
    logger.info(event)
    if event['queryStringParameters'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    req_params = event['queryStringParameters']
    param_checker = TableOrderParamCheck(req_params)

    if error_msg := param_checker.check_api_order_info():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    try:
        payment_info = get_order_info(req_params)
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response('ERROR')

    return utils.create_success_response(
        json.dumps(payment_info, default=utils.decimal_to_int,
                   ensure_ascii=False))
