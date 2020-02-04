import json
class Flex:
    bubble_json_temp = '''{
      "type": "bubble",
<<<<<<< HEAD
=======
      "size": "kilo",
>>>>>>> dev
      "header": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "*event_date",
            "margin": "none",
            "weight": "bold",
<<<<<<< HEAD
            "color": "#FFFFFF"
=======
            "color": "#FFFFFF",
            "size": "xl"
>>>>>>> dev
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
            "size": "lg",
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
        bubble_json = self.bubble_json_temp.replace("*img_url", event['img_url']).replace('*event_date', str_date).replace('*event_name', event['event_name']).replace('*event_url', event['event_url'])
        return bubble_json
