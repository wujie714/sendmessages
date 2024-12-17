from channel.wework.wework_channel import WeworkChannel
from channel.wework.wework_channel import get_with_retry
import os

from channel.chat_channel import ChatChannel
from channel.wework.run import wework
from loguru import logger
import requests
import tempfile
from plugins.sendmessages.sendmessages import sendType

class MyGISWeworkChannel(ChatChannel):
    def __init__(self):
        # super().__init__()
        from channel.wework.wework_channel import WeworkChannel
        self.channel = WeworkChannel
    def sendAllFriends(self,content,all=False):
        contacts=self.get_contacts()
        iNum=0
        for contact in contacts:
            logger.info("contact:{}".format(contact))
            # wework.send_room_at_msg()
            self.send_rawmsg(content,contact["conversation_id"])
            iNum+=1
        return "发送了 {} 个好友".format(iNum)

    def sendAllRooms(self,content,all:sendType=sendType.OWNER):
        rooms=self.get_rooms()
        iNum = 0
        for room in rooms:
            logger.info("room:{}".format(room))

        return "发送了 {} 个群!".format(iNum)


    # def send_msg(self, msg_type, content, to_user_name, at_content=None):
    #     pass
    def get_rooms(self):
        rooms = get_with_retry(wework.get_rooms)["room_list"]
        return rooms
    def get_contacts(self):
        contacts = get_with_retry(wework.get_external_contacts)["user_list"]
        return contacts

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
        media_type =self.getMessageType(content)
        self.send_msg(msg_type=media_type,content=content,to_user_name=to_user_name)

    def send_msg(self, msg_type, content, to_user_name, at_content=None):
        """
        实际itchat发送消息函数
        :param msg_type: 消息类型
        :param content: 消息内容
        :param to_user_name: 接收者的 UserName
        :param at_content: @的内容
        """
        logger.info("msg_type:{},content:{}".format(msg_type,content))
        network =False
        if content.startswith(("http://", "https://")):
            network=True

        if msg_type == 'text':
            if at_content:
                wework.send_text(to_user_name, f'{at_content} {content}')
            else:
                wework.send_text(to_user_name,content)
        elif msg_type in ['img', 'video', 'file']:
            # 如果是图片、视频或文件,先下载到本地
            local_file_path = content
            absolute_path =local_file_path
            if network==True:
                local_file_path = self._download_file(content)

            #获取绝对路径
            current_directory = os.getcwd()
            # 拼接得到完整的绝对路径
            absolute_path = os.path.join(current_directory, local_file_path)
            absolute_path = os.path.abspath(absolute_path)
            logger.info("absolute_path:{}".format(absolute_path))

            if local_file_path:
                if msg_type == 'img':

                    wework.send_image(to_user_name,file_path=absolute_path)
                elif msg_type == 'video':
                    wework.send_video(to_user_name,file_path=absolute_path)
                elif msg_type == 'file':
                    wework.send_file(to_user_name, file_path=absolute_path)
                # 发送完成后删除本地临时文件
                if network == True:
                    os.remove(absolute_path)
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
