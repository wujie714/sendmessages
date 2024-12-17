from lib import itchat
from channel.chat_channel import ChatChannel
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
from plugins import *
import time
from loguru import logger
from config import conf, load_config, global_config
import requests
import random
from channel.chat_channel import check_contain,check_prefix
from plugins.sendmessages.sendmessages import sendType

class MyGISItChannel(ChatChannel):
    mygis_sleep_minsecond=0
    mygis_sleep_maxsecond=1
    mygis_groups_whitelist=["吴杰共享群"]
    mygis_groups_blacklist=[]
    mygis_friends_whitelist=["吴杰.九鼎图业"]
    mygis_friends_blacklist=[]
    pItchat=None
    def __init__(self):
        # super().__init__()
        from lib import itchat
        self.pItchat =itchat
    def add_member_into_chatroom(self, roomname,UserName):
        chatrooms = self.pItchat.get_chatrooms(update=True)
        logger.info("room name:{}".format(roomname))
        for chatroom in chatrooms:
            if chatroom["NickName"] == roomname:
                logger.info("chatroom:{}".format(chatroom))
                self.pItchat.add_member_into_chatroom(chatroom["UserName"], UserName)
                break

        return "no room!"

    def sendAllRooms(self, content,all):
        """
        使用 itchat 发送消息的逻辑
        """
        global media_type, content_at
        # 判断消息类型
        media_type = self.getMessageType(content)
        iSendNum = 0
        strRooms =[]
        try:
            chatrooms=self.pItchat.get_chatrooms(update=True)
            for chatroom in chatrooms:
                # logger.info("chatroom:{}".format(chatroom))
                logger.info("chatroom:{}".format(chatroom["NickName"]))

                user_id=self.pItchat.instance.storageClass.userName
                bIsOwner =False
                if "ChatRoomOwner" in chatroom:
                    bIsOwner = (user_id == chatroom["ChatRoomOwner"])
                    # logger.info("name:{},user_id:{},ChatRoomOwner:{}".format(chatroom["NickName"],user_id,chatroom["ChatRoomOwner"]))
                # room_ownerid=chatroom["ChatRoomOwner"]


                if (all==sendType.OWNER.value and bIsOwner) \
                        or (all==sendType.ALL.value) \
                        or (all==sendType.WHITELIST.value and chatroom["NickName"] in self.mygis_groups_whitelist):

                    logger.info("发送...{}".format(chatroom["NickName"]))
                    strRooms.append(chatroom["NickName"])
                    self.send_msg(msg_type=media_type, content=content,
                                          to_user_name=chatroom.UserName)
                    iSendNum += 1

                    random_number = random.randint(self.mygis_sleep_minsecond, self.mygis_sleep_maxsecond)
                    logger.info("等待...{}秒".format(random_number))
                    time.sleep(random_number)

        except Exception as e:
            logger.error(f"处理消息时发生异常: {e}")
            # raise e

        retMsg = "共发送：{}个群,分别为:{}".format(iSendNum,strRooms)
        return retMsg

    def sendAllFriends(self, content,all):
        """
        使用 itchat 发送消息的逻辑
        """
        global media_type, content_at

        # 判断消息类型
        media_type = self.getMessageType(content)

        iSendNum = 0
        strFriends = []
        try:
            friends=self.pItchat.get_friends(update=True)
            for friend in friends:
                if (all==sendType.ALL.value) or(all==sendType.WHITELIST.value and friend["NickName"] in self.mygis_friends_whitelist):
                    logger.info("发送...{}".format(friend["NickName"]))

                    self.send_msg(msg_type=media_type, content=content,
                                          to_user_name=friend.UserName)
                    iSendNum+=1
                    strFriends.append(friend["NickName"])
                    random_number = random.randint(self.mygis_sleep_minsecond, self.mygis_sleep_maxsecond)
                    logger.info("等待...{}秒".format(random_number))
                    time.sleep(random_number)

        except Exception as e:
            logger.error(f"处理消息时发生异常: {e}")
            # raise e

        retMsg = "共发送了：{} 个朋友，分别是:{}".format(iSendNum,strFriends)
        return retMsg
    def getMessageType(self, content):
        global media_type
        # 判断消息类型
        if content.startswith(("http://", "https://")):
            # 网络
            if content.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".img")):
                media_type = "img"
            elif content.lower().endswith((".mp4", ".avi", ".mov",)):
                media_type = "video"
            elif content.lower().endswith((".pdf", ".doc", ".docx", ".xls", "xlsx", ".zip", ".rar", "txt")):
                media_type = "file"
            else:
                media_type = "text"
                # logger.warning(f"不支持的文件类型: {content}")
        elif os.path.exists(content):
            if content.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".img")):
                media_type = "img"
            elif content.lower().endswith((".mp4", ".avi", ".mov",)):
                media_type = "video"
            elif content.lower().endswith((".pdf", ".doc", ".docx", ".xls", "xlsx", ".zip", ".rar", "txt")):
                media_type = "file"
            else:
                media_type = "text"
                # logger.warning(f"不支持的文件类型: {content}")
        else:
            media_type = "text"

        return media_type
    def send_rawmsg(self, content, to_user_name):
        global media_type, content_at
        # 判断消息类型
        media_type =self.getMessageType()
        self.send_msg(msg_type=media_type,content=content,to_user_name=to_user_name)

    def send_msg(self, msg_type, content, to_user_name, at_content=None):
        """
        实际itchat发送消息函数
        :param msg_type: 消息类型
        :param content: 消息内容
        :param to_user_name: 接收者的 UserName
        :param at_content: @的内容
        """
        network =False
        if content.startswith(("http://", "https://")):
            network=True

        if msg_type == 'text':
            if at_content:
                self.pItchat.send(f'{at_content} {content}', to_user_name)
            else:
                self.pItchat.send(content, to_user_name)
        elif msg_type in ['img', 'video', 'file']:
            # 如果是图片、视频或文件,先下载到本地

            local_file_path = content
            if network==True:
                local_file_path = self._download_file(content)

            if local_file_path:
                # self.pItchat.send(at_content, to_user_name)
                if msg_type == 'img':
                    self.pItchat.send_image(local_file_path, to_user_name)
                elif msg_type == 'video':
                    self.pItchat.send_video(local_file_path, to_user_name)
                elif msg_type == 'file':
                    self.pItchat.send_file(local_file_path, to_user_name)
                # 发送完成后删除本地临时文件
                if network == True:
                    os.remove(local_file_path)
            else:
                raise ValueError(f"无法下载文件: {content}")

    def _download_file(self, url):
        """
        下载文件到本地
        :param url: 文件的URL
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = os.path.basename(url)
                logger.info("file_name:{}".format(file_name))
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return file_name
            return None
        except Exception as e:
            logger.error(f"下载文件时发生异常: {e}")
            return None



    # 处理好友申请
    def _build_friend_request_reply(self, context):
        if isinstance(context.content, dict) and "Content" in context.content:
            logger.info("friend request content: {}".format(context.content["Content"]))
            logger.info("accept_friend_commands: {}".format(self.conf["accept_friend_commands"]))

            # if context.content["Content"] in conf().get("accept_friend_commands", []):
            bIsContain = self.check_contain(context.content["Content"], self.conf["accept_friend_commands"])
            if False:
                self.pItchat.accept_friend(userName=context.content["UserName"], v4=context.content["Ticket"])
                self.pItchat.send(self.conf["accept_friend_msg"], toUserName=context.content["UserName"])
                # self.channel.send(self.conf["mygis_help"], toUserName=context.content["UserName"])
            #
            # logger.info("bIsContain:{}".format(bIsContain))

            # return Reply(type=ReplyType.TEXT, content=self.conf["accept_friend_msg"])


            return Reply(type=ReplyType.ACCEPT_FRIEND, content=bIsContain)


        else:
            logger.error("Invalid context content: {}".format(context.content))
            return None

    # 判断是否含有关键字
    def check_contain(self, msg, keys_list):
        for key in keys_list:
            if key.upper() in msg.upper():
                return True
        return False