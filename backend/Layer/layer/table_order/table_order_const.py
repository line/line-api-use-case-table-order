import os
from common import const

const.FLEX_COUPON = {
        "type": "flex",
        "altText": "ご来店ありがとうございました。またのご来店をお待ちしています。次回ご来店時に使用できるクーポンを発行します。",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "10%割引クーポン発行",
                        "size": "sm",
                        "color": "#36DB34",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "Use Case 居酒屋",
                        "size": "xxl",
                        "weight": "bold"
                    }
                ],
                "paddingBottom": "2%"
            },
            "hero": {
                "type": "image",
                "url": "https://media.istockphoto.com/vectors/percent-off-sale-and-discount-price-tag-icon-or-sticker-vector-vector-id1194658271?s=2048x2048",
                "size": "full",
                "aspectRatio": "2:1",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "label": "Action",
                    "uri": os.environ.get("LIFF_URL")
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ご利用ありがとうございました。\n\n次回来店時に本メッセージを店員に提示していただければ、会計から10 % 割引させていただきます。",  # noqa:E501
                                "wrap": True,
                                "size": "sm",
                                "color": "#767676"
                            }
                        ]
                    }
                ],
                "paddingTop": "5%"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "spacer",
                        "size": "md"
                    }
                ],
                "flex": 0
            }
        }
    }
