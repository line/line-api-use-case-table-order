import json
import os
import logging

from common import (common_const, utils)
from validation.table_order_param_check import TableOrderParamCheck
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501


# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
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
    該当の会計情報を会計済みにする
    Parameters
    ----------
    event : dict
        POST時に渡されたパラメータ
    context : dict
        コンテキスト内容
    Returns
    -------
    なし（共通項目のみ）
    """
    # パラメータログ
    logger.info(event)
    if event['body'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    req_body = json.loads(event['body'])

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(req_body)

    if error_msg := param_checker.check_api_payment_confirm_nolinepay():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    payment_id = req_body['paymentId']
    transaction_id = 99999999999999

    try:
        # データを支払済みに更新する
        payment_order_table_controller.update_payment_info(
            payment_id, transaction_id)
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response("Error")

    return utils.create_success_response("")
