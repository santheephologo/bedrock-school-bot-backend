from sqlalchemy.orm import Session
from main.models import Bot, Client, ClientBot  
import uuid

class BotService:

    def __init__(self):
        pass
    
    @property
    def db_session(self):
        from main import db 
        return db.session

    def botRegister(self, name, agent_id, alias_id):
        try:
            existing_bot = self.db_session.query(Bot).filter_by(name=name).first()
            if existing_bot:
                return None
            else:
                bot = Bot(
                    name=name,
                    agent_id=agent_id,
                    alias_id=alias_id,
                    is_active=True,
                )
                self.db_session.add(bot)
                self.db_session.commit()
                return True
        except Exception as e:
            self.db_session.rollback()
            print(f"Error in bot registration: {e}")
            return None

    def updateBot(self, name, bot_id, agent_id, alias_id):
        try:
            bot = self.db_session.query(Bot).filter_by(id=int(bot_id)).first()
            if bot:
                bot.name = name
                bot.agent_id = agent_id
                bot.alias_id = alias_id
                self.db_session.commit()
                return True
            return False
        except Exception as e:
            self.db_session.rollback()
            print(f"Error in updating bot: {e}")
            return None

    def fetchBots(self):
        try:
            bots = self.db_session.query(Bot).all()
            client_bots = self.db_session.query(ClientBot).all()
            
            bot_user_count = {int(bot.id): 0 for bot in bots} 
            for client_bot in client_bots:
                if client_bot.bot_id in bot_user_count:
                    bot_user_count[client_bot.bot_id] += 1
            bot_list = []
            for bot in bots:
                bot_json = bot.to_json()
                bot_json['no_of_users'] = bot_user_count.get(bot_json['id'], 0) 
                bot_list.append(bot_json)                        
            return bot_list
        except Exception as e:
            print(f"Error fetching bots: {e}")
            return None

    def fetchDashboard(self):
        try:
            client_count = self.db_session.query(Client).count()
            bot_count = self.db_session.query(Bot).count()
            return {
                "client_count": client_count,
                "bot_count": bot_count
            }
        except Exception as e:
            print(f"Error fetching dashboard data: {str(e)}")
            return None

    def returnBot(self, bot_id):
        try:
            bot = self.db_session.query(Bot).filter_by(id=int(bot_id)).first()
            return bot.to_json() if bot else None
        except Exception as e:
            print(f"Error fetching bot: {e}")
            return None

    def deleteBot(self, bot_id):
        try:
            bot = self.db_session.query(Bot).filter_by(id=int(bot_id)).first()
            if bot:
                self.db_session.delete(bot)
                self.db_session.commit()
                return True
            return False
        except Exception as e:
            self.db_session.rollback()
            print(f"Error deleting bot: {e}")
            return None


# from main.models.bot import Bot
# from main.models.client import Client, ClientBot
# import bcrypt

# class BotService:
    
#     def botRegister(self, name, agent_id, alias_id):
#         try:
#             bot= Bot(
#             name=name,
#             agent_id=agent_id,
#             alias_id=alias_id,
#             is_active=True,
#             )
#             bot.save()
#             return bot
#         except Exception:
#             return None

#     def updateBot(self, name, bot_id, agent_id, alias_id):
#         try:
#             bot = Bot.objects.get(id=bot_id)
#             initial_name = bot.name
#             if(initial_name!=name):
#                 print("new name ")
#                 bot.name = name
#                 bot.agent_id = agent_id
#                 bot.alias_id = alias_id
#                 bot.save()
#                 clients = Client.objects.all()
#                 if clients:
#                     bot_updated = False
#                     for client in clients:
#                         for bot in client.bots:
#                             if bot.id == bot_id:
#                                 bot.name = name
#                                 bot_updated = True
#                     client.save()
#                 return True
#             else:
#                 print("same name")
#                 bot.agent_id = agent_id
#                 bot.alias_id = alias_id
#                 bot.save()
#                 return True
#         except Exception as e:
#             print("error ", str(e) )
#             return None

#     def fetchBots(self):
#         # clients = Client.objects.all()
#         # bots = Bot.objects.all()
#         # return [bot.to_json() for bot in bots]
#         clients = Client.objects.all()  
#         bots = Bot.objects.all() 
#         bot_user_count = {str(bot.id): 0 for bot in bots}  
#         print("bot user cnt ", bot_user_count)
#         for client in clients:
#             for client_bot in client.bots:
#                 if client_bot.id in bot_user_count:
#                     # print("bot ", client_bot.id, "in use")
#                     bot_user_count[client_bot.id] += 1 
#                     # print("bot cnt ", bot_user_count)

#         bot_list = []
#         for bot in bots:
#             bot_json = bot.to_json()
#             bot_json['no_of_users'] = bot_user_count.get(bot_json['id'], 0) 
#             bot_list.append(bot_json)

#         return bot_list

#     def fetchDashboard(self):
#         try:
#             client_count = Client.objects.count()
#             bot_count = Bot.objects.count()
#             return {
#                 "client_count": client_count,
#                 "bot_count": bot_count
#             }
#         except Exception as e:
#             print(f"Error fetching dashboard data: {str(e)}")
#             return None
        
#     def returnBot(self, bot_id):
#         try:
#             bot = Bot.objects.get(id=bot_id)
#             return bot.to_json()
#         except Bot.DoesNotExist:
#             return None
             
#     def updateClientToken(self, username, addition):
#         try:
#             client = Client.objects.get(username=username)
#             # client.update(inc__tkns_remaining=add_tkn)
#             client.tkns_remaining += addition
#             client.save()
#             return True
#         except Client.DoesNotExist:
#             return None        
    
#     def deleteBot(self, botId):
#         try:
#             bot = Bot.objects.get(id=botId)
#             bot.delete()
#             return True
#         except bot.DoesNotExist:
#             return None          
