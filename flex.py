import json
from linebot.models import FlexSendMessage



class Flex:

    start_flex_temp='''
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "新着イベント",
          "text": "新着のイベントを教えて"
        },
        "style": "primary",
        "color": "#ff7f50"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "日時から検索",
          "text": "日時から探したい"
        },
        "style": "primary"
      }
    ]
  }
}
    '''

    from_datepicker_temp = '''
    {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "何日から探す？",
        "weight": "bold",
        "size": "xl"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "md",
        "action": {
          "type": "datetimepicker",
          "mode": "date",
          "label": "日付を選択",
          "data": "from_date_message"
        },
        "color": "#ff7f50"
      }
    ],
    "flex": 0
  }
}'''

    to_datepicker_temp = '''
    {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "何日まで探す？",
        "weight": "bold",
        "size": "xl"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "md",
        "action": {
          "type": "datetimepicker",
          "mode": "date",
          "label": "日付を選択",
          "data": "to_date_message:*fromdate"
        }
      }
    ],
    "flex": 0
  }
}
    '''
    bubble_json_temp = '''{
      "type": "bubble",
      "size": "micro",
      "header": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "*event_date",
            "margin": "none",
            "weight": "bold",
            "color": "#FFFFFF",
            "size": "xl"
          }
        ],
        "backgroundColor": "#ff7f50"
      },
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": "*img_url"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "*event_name",
            "wrap": true,
            "weight": "regular",
            "size": "md",
            "maxLines": 3,
            "color": "#FFFFFF"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "Detail",
              "uri": "*event_url"
            },
            "color": "#ffffff1A",
            "style": "primary"
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#464F69"
        },
        "footer": {
          "backgroundColor": "#464F69"
        }
      }
    },'''
    # Atention! , follows from backside

    def __init__(self):
        pass

    def set_event_data(self, event):
        str_date = event['event_date'].strftime('%m/%d')
        bubble_json = self.bubble_json_temp.replace("*img_url", event['img_url']).replace(
            '*event_date', str_date).replace('*event_name', event['event_name']).replace('*event_url', event['event_url'])
        return bubble_json

    def gen_from_datepicker(self):
        from_datepicker_json = json.loads(self.from_datepicker_temp)
        from_datepicker_flex = FlexSendMessage(alt_text="from_datepicker",contents=from_datepicker_json)
        print(from_datepicker_flex)
        return from_datepicker_flex
        
    def gen_to_datepicker(self,from_date):
        to_datepicker_text = self.to_datepicker_temp.replace("*fromdate",from_date.isoformat())
        to_datepicker_json = json.loads(to_datepicker_text)
        to_datepicker_flex = FlexSendMessage(alt_text="to_datepicker",contents=to_datepicker_json)
        return to_datepicker_flex
    
    def gen_start_flex(self):
        start_flex_json = json.loads(self.start_flex_temp)
        start_flex = FlexSendMessage(
            alt_text="start_flexmenu", contents=start_flex_json)
        return start_flex
