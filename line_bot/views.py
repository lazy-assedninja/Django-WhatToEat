import os
from django.http import HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import *
from .models import *

# Init
file_host = 'https://app.whattoeat.work/File/Store/'
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_LONG_TOKEN'))
web_hook_handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


def webhook(request):
    try:
        # Signature
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        web_hook_handler.handle(body, signature)
    except LineBotApiError as e:
        print(e.error.message)
    return HttpResponse("Success.")


@web_hook_handler.add(MessageEvent, message=TextMessage)
def echo(event):
    try:
        message = event.message.text
        if message == 'Recommend':
            stores = get_stores()
            send_recommend_stores(event.reply_token, stores)
    except LineBotApiError as e:
        print(str(e))


@web_hook_handler.add(FollowEvent)
def follow(event):
    try:
        # Get line user's information
        user_name = line_bot_api.get_profile(
            event.source.sender_id).display_name

        # Send welcome message
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Hello, " + user_name + "\n Thanks for the following. \U001000A4"))
    except LineBotApiError as e:
        print(str(e))


@web_hook_handler.add(PostbackEvent)
def post_back(event):
    try:
        store_name = event.postback.data
        store = get_information(store_name)
        if store.count() != 0:
            send_information(event.reply_token, store[0])
    except LineBotApiError as e:
        print(str(e))


def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))


def send_recommend_stores(reply_token, stores):
    try:
        carousel = []
        for store in stores:
            bubble = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    padding_all='0px',
                    contents=[
                        ImageComponent(
                            url=file_host + store.picture,
                            size='full',
                            aspect_mode='cover',
                            aspect_ratio='1:1',
                            gravity='center'
                        ),
                        ImageComponent(
                            url='https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip15.png',
                            position='absolute',
                            aspect_mode='fit',
                            aspect_ratio='1:1',
                            offset_start='0px',
                            offset_top='0px',
                            offset_bottom='0px',
                            offset_end='0px',
                            size='full'
                        ),
                        BoxComponent(
                            layout='horizontal',
                            position='absolute',
                            offset_bottom='0px',
                            offset_start='0px',
                            offset_end='0px',
                            padding_all='20px',
                            contents=[
                                BoxComponent(
                                    layout='vertical',
                                    spacing='xs',
                                    contents=[
                                        BoxComponent(
                                            layout='horizontal',
                                            contents=[
                                                TextComponent(
                                                    text=store.name,
                                                    size='xl',
                                                    color='#FFFFFF'
                                                )
                                            ]
                                        ),
                                        BoxComponent(
                                            layout='baseline',
                                            spacing='xs',
                                            contents=[
                                                IconComponent(
                                                    url='https://scdn.line-apps.com/n/channel_devcenter/img/fx'
                                                        '/review_gold_star_28.png',
                                                    margin='md',
                                                    offset_top='2px'
                                                ),
                                                TextComponent(
                                                    text=str(store.star),
                                                    color='#A9A9A9',
                                                    margin='sm',
                                                    offset_top='1px'
                                                )
                                            ]
                                        ),
                                        BoxComponent(
                                            layout='horizontal',
                                            contents=[
                                                TextComponent(
                                                    text=store.address,
                                                    color='#A9A9A9'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    action=PostbackAction(
                        label='Show Information',
                        data=store.name,
                        display_text=store.name
                    )
                )
            )
            carousel.append(bubble)

        line_bot_api.reply_message(reply_token,
                                   FlexSendMessage(alt_text='Recommend', contents=CarouselContainer(contents=carousel)))
    except LineBotApiError as e:
        print(str(e))


def send_information(reply_token, store):
    try:
        carousel = []
        bubble = BubbleContainer(
            hero=ImageComponent(
                url=file_host + store.picture,
                size='full',
                aspect_ratio='20:12',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text=store.name,
                        weight='bold',
                        size='xl'
                    ),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(
                                url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png'
                            ),
                            TextComponent(
                                text=str(store.star),
                                size='sm',
                                color='#999999',
                                offset_start='5px',
                                offset_top='-2px'
                            )
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#AAAAAA',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=store.address,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ]
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#AAAAAA',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='24 hour',
                                        wrap=True,
                                        color='#AAAAAA',
                                        size='sm',
                                        flex=5
                                    )
                                ]
                            )
                        ]
                    )
                ],
                action=PostbackAction(
                    label='Show Information',
                    data=store.name,
                    display_text=store.name
                )
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        height='sm',
                        style='primary',
                        color='#5061AE',
                        action=URIAction(
                            uri="https://www.google.com/maps/search/?api=1&query=" + store.latitude + ","
                                + store.longitude + "&query_place_id=" + store.place_id,
                            label='Location'
                        )
                    ),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=MessageAction(
                            label='No website.',
                            text='No website'
                        ) if store.website is None else URIAction(
                            label='Website',
                            uri=store.website
                        )
                    )
                ]
            )
        )
        carousel.append(bubble)

        line_bot_api.reply_message(reply_token,
                                   FlexSendMessage(alt_text='Recommend', contents=CarouselContainer(contents=carousel)))
    except LineBotApiError as e:
        print(str(e))


def get_stores():
    try:
        stores = Store.objects.select_related('tag').filter(tag__id=2)
        return stores
    except Exception as e:
        print(str(e))


def get_information(store_name):
    try:
        stores = Store.objects.select_related('tag').filter(name=store_name)
        return stores
    except Exception as e:
        print(str(e))
