from linebot.models import(
    BoxComponent,
    TextComponent,
    SeparatorComponent
)
from linebot.models import *
from psycopg2 import *
import json
import pprint


def gen_events_carousel(events):
    # events : dict in list
    messages = []
    for i in range((len(events)+9)//10):
        carousel_template_message = TemplateSendMessage(
            alt_text='Events',
            template=CarouselTemplate(
                columns=gen_events_columns(events[i*10:(i+1)*10])
            )
        )
        messages.append(carousel_template_message)
    return messages


# 10　ずつ生成する。


def gen_events_columns(part_of_events):
    columns = []
    for event in part_of_events:
        str_date = event['event_date'].strftime('%m/%d')
        column = CarouselColumn(
            thumbnail_image_url=event['img_url'],
            title=str_date,
            text=event['event_name'],
            actions=[
                URIAction(
                    label="detail",
                    uri=event['event_url']
                )
            ]
        )
        columns.append(column)
    return columns


def ask_fromdate():
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title='いつから探す？',
            text='以下より選択してね。',
            actions=[
                 DatetimePickerAction(
                     label='Select FromDate',
                     data="from_date_message",
                     mode="date",
                 )
            ])
    )
    return message


def ask_todate(from_date):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title='いつまで探す？',
            text='以下より選択してね。',
            actions=[
                 DatetimePickerAction(
                     label='Select ToDate',
                     data=f"to_date_message:{from_date.isoformat()}",
                     mode="date",
                 )
            ])
    )
    return message


def gen_events_flex_carousel_list(events):
    carousels = []
    for i in range((len(events)+9)//10):
        carousels.append(gen_events_flex_carousel(events[i*10:(i+1)*10]))
    return carousels


def gen_events_flex_carousel(part_of_events):
    bubbles = str()
    carousel = '''{
        "type":"carousel",
        "contents":[
    '''
    for event in part_of_events:
        bubbles += gen_flex_bubble(event)

    bubbles = bubbles[:-1]
    carousel += (bubbles + "]}")
    print(carousel)

    carousel = FlexSendMessage.new_from_json_dict(json.loads(carousel))
    return carousel


# json convert to python dict
# return that python dict
def gen_flex_bubble(event):
    json_data = """
    {"type": "bubble",
      "size": "mega",
      "hero": {
        "type": "image",
        "url": \"*img_url\",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "margin": "none",
        "size": "full"
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
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "*event_date",
                    "size": "md",
                    "weight": "bold",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "xs"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "*event_name",
                "size": "lg",
                "align": "center"
              }
            ]
          }
        ],
        "spacing": "md",
        "paddingAll": "13px",
        "borderColor": "#808080"
      },
      "footer": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "de",
            "align": "center",
            "weight": "bold",
            "color": "#4169E1"
          }
        ],
        "action": {
          "type": "uri",
          "label": "action",
          "uri": "*event_url"
        }
      },
      "styles": {
        "footer": {
          "separator": true
        }
      }
    },"""
    str_date = event['event_date'].strftime('%m/%d')
    json_date = json_data.replace("*img_url", event['imgぎ_url'])#.replace('*event_date', str_date).replace('*event_name', event['event_name']).replace('*event_url', event['event_url'])
    return json_data
