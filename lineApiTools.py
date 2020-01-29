from linebot.models import(
    BoxComponent,
    TextComponent,
    SeparatorComponent
)
from linebot.models import *
from psycopg2 import *


def gen_events_carousel(events):
    # events : dict in list
    messages = []
    for i in range(len(events)//10):
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