import requests
import json
from .ReolConsts import LARK_API


def sync_success(repos_num, sync_time, time_cost):
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "red",
                "title": {
                    "tag": "plain_text",
                    "content": "🔥🔥🔥 恭喜这位爷，您的仓库刚刚同步成功了🔥🔥🔥 "
                }
            },
            "elements": [
                {
                    "tag": "img",
                    "img_key": "img_v3_025j_ab54cb72-06c9-4b82-a656-3f6f9c04250g",
                    "alt": {
                        "tag": "plain_text",
                        "content": ""
                    },
                    "mode": "fit_horizontal",
                    "preview": True,
                    "compact_width": False
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "现在即可查看最新同步后的代码，或继续编辑仓库配置",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "default",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": f"**当前仓库数量\n<font color='red'> {repos_num} </font>**",
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": f"**每日同步时间\n<font color='green'> {sync_time}</font>**",
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": f"**本次同步耗时\n<font color='green'> {time_cost} mins</font>**",
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "前往代码浏览网站，迅速品尝新鲜同步的代码"
                    },
                    "extra": {
                        "tag": "button",
                        "text": {
                            "tag": "lark_md",
                            "content": "现在就浏览代码"
                        },
                        "type": "primary",
                        "multi_url": {
                            "url": "http://10.114.40.26:8529/source/",
                            "pc_url": "",
                            "android_url": "",
                            "ios_url": ""
                        }
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "终于同步完了呜呜呜，可我还想再改一下配置"
                    },
                    "extra": {
                        "tag": "button",
                        "text": {
                            "tag": "lark_md",
                            "content": "再一次修改配置"
                        },
                        "type": "primary",
                        "multi_url": {
                            "url": "http://10.114.40.26:5173/",
                            "pc_url": "",
                            "android_url": "",
                            "ios_url": ""
                        }
                    }
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "💡 [温馨提示] 如果觉得好用，请肆意传播"
                        }
                    ]
                }
            ]
        }
    }
    return json.dumps(card)


def pray_sincerely(pray_words):
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": f"亲爱的<at id=erwei.luo></at>:\n{pray_words}"
                },
                {
                    "tag": "hr"
                },
                {
                    "elements": [
                        {
                            "content": "[来自不知名生物]",
                            "tag": "lark_md"
                        }
                    ],
                    "tag": "note"
                }
            ],
            "header": {
                "template": "yellow",
                "title": {
                    "content": "【尊敬的伟大先知】远方依稀传来不知名生物的低声祈祷",
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(card)


def send_notification(msg_json):
    try:
        response = requests.post(LARK_API, data=msg_json, headers={
                                 "Content-Type": "application/json"})
    except Exception as e:
        print(e)
        return False
    if response.status_code == 200:
        return True
