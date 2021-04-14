import json
import logging
import os
import sys

from table_order import table_order_const
from common import (common_const, line, utils)
from linepay import LinePayApi
from validation.table_order_param_check import TableOrderParamCheck
from common.channel_access_token import ChannelAccessToken
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501


# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# LINE Pay API
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
channel_access_token_controller = ChannelAccessToken()

# LINE BOTリソースの宣言
CHANNEL_ID = os.getenv('LINE_CHANNEL_ID', None)
if CHANNEL_ID is None:
    logger.error('Specify CHANNEL_ID as environment variable.')
    sys.exit(1)


def send_messages(body):
    """
    OAにメッセージを送信する
    Parameters
    ----------
    body:dict
        該当ユーザーの支払情報
    Returns
    -------
    なし
    """
    flex_obj = table_order_const.const.FLEX_COUPON
    # DBより短期チャネルアクセストークンを取得
    channel_access_token = channel_access_token_controller.get_item(CHANNEL_ID)
    if channel_access_token is None:
        logger.error(
            'CHANNEL_ACCESS_TOKEN in Specified CHANNEL_ID: %s is not exist.',
            CHANNEL_ID)
    else:
        line.send_push_message(
            channel_access_token['channelAccessToken'], flex_obj, body['userId'])


def lambda_handler(event, context):
    """
    LINE Pay API(confirm)の処理結果を返す
    Parameters
    ----------
    event : dict
        POST時に渡されたパラメータ
    context : dict
        コンテキスト内容。
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

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(req_body)

    if error_msg := param_checker.check_api_payment_confirm():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    payment_id = req_body['paymentId']
    transaction_id = int(req_body['transactionId'])

    try:
        # 注文履歴から決済金額を取得
        payment_info = payment_order_table_controller.get_item(
            payment_id)
        amount = float(payment_info['amount'])
        currency = 'JPY'
        # 会計テーブルを更新
        payment_order_table_controller.update_payment_info(
            payment_id, transaction_id)
        # LINE PayAPI予約処理
        try:
            linepay_api_response = api.confirm(
                transaction_id, amount, currency)
            res_body = json.dumps(linepay_api_response)
        except Exception as e:
            # LINE Pay側でエラーが発生した場合は会計テーブルを戻す
            logger.error('Occur Exception: %s', e)
            transaction_id = 0
            payment_order_table_controller.update_payment_info(
                payment_id, transaction_id)
            return utils.create_error_response("Error")
        # プッシュメッセージ送信
        send_messages(payment_info)

    except Exception as e:
        if transaction_id is not None and transaction_id == 0:
            logger.critical(
                'payment_id: %s could not update, please update transaction_id = 0 manually and confirm the payment',  # noqa 501
                payment_id)
        else:
            logger.error('Occur Exception: %s', e)
        return utils.create_error_response("Error")

    return utils.create_success_response(res_body)
