from main.models.client import Client
from main.models.client_bot import ClientBot
import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
class ClientService:
    
    def __init__(self):
        pass
    
    @property
    def db_session(self):
        from main import db  
        return db.session

    def clientRegister(self, username, email, password, first_name, last_name):
        try:
            client = Client(
                username=username,
                email=email,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # Decode to string
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            self.db_session.add(client)  
            self.db_session.commit()      
            return True     
        except IntegrityError as e:
            self.db_session.rollback()    
            print(f"IntegrityError: {str(e)}")
            return None
        except Exception as e: 
            self.db_session.rollback()     
            print(str(e))
            return None

    def clientLogin(self, email, password):
        try:
            client = self.db_session.query(Client).filter_by(email=email).first() 
            
            if client is None:
                return False
            
            if bcrypt.checkpw(password.encode('utf-8'), client.password.encode('utf-8')):
                return True  
            else:
                return False
        except Exception as e:
            print(str(e))
            return False              

    def fetchClients(self):
        try:
            clients = self.db_session.query(Client).all()
            client_bots = self.db_session.query(ClientBot).all()

            # Initialize the bots list for each client
            clients_with_bots = []
            for client in clients:
                client_json = client.to_json()
                client_json['bots'] =[]
                clients_with_bots.append(client_json)

            for bot in client_bots:
                for client in clients_with_bots:
                    if bot.client_id == int(client_json['id']):
                        client_json['bots'].append(bot.to_json())
       
            return clients_with_bots
        except Exception as e:
            print("Error:", str(e))
            return False

    def returnClient(self, username):
        try:
            client = self.db_session.query(Client).filter_by(username=username).first() 
            client_bots = self.db_session.query(ClientBot).filter_by(client_id=client.id).all()
            client_bots_json = [client_bot.to_json() for client_bot in client_bots]
            client_json = client.to_json()
            client_json['bots'] = client_bots_json
            print(client_json)
            return client_json
        except Exception as e:
            print(str(e))
            return None  

    def returnTokenInfo(self, username):
        try:
            client = self.db_session.query(Client).filter_by(username=username).first()  
            if client:
                return (
                    f"Allocated tokens: {client.tkns_remaining + client.tkn_used}",
                    f"Remaining tokens: {client.tkns_remaining}",
                    f"Tokens used: {client.tkn_used}"
                )
            return None 
        except Exception as e:
            print(str(e)) 
            return None        

    def updateClientBotToken(self, client_id, bot_id, addition):
        try:
            print(client_id, bot_id,addition)
            client_bot = self.db_session.query(ClientBot).filter_by(client_id=int(client_id), bot_id=int(bot_id)).first()  
            if client_bot:
                client_bot.tkns_remaining += addition 
                self.db_session.commit() 
                return True  
            return None  
        except Exception as e:
            print(str(e))  
            self.db_session.rollback() 
            return None

    def addBot(self, client_id, bot_name, bot_id, tkns_remaining, tkns_used):
        try:
            client_bot = ClientBot(
                    client_id=int(client_id),
                    bot_id=int(bot_id),
                    name=bot_name,
                    tkns_remaining=int(tkns_remaining),
                    tkns_used=int(tkns_used)
                )
            self.db_session.add(client_bot)  
            self.db_session.commit()  
            return True 
        except Exception as e:
            print("@109",str(e)) 
            self.db_session.rollback()  
            return None

    def deleteClientBot(self, client_id, bot_id):
        try:
            client_bot = self.db_session.query(ClientBot).filter_by(client_id=int(client_id), bot_id=int(bot_id)).first()  
            if(client_bot):
                self.db_session.delete(client_bot)
                self.db_session.commit()  
                return True
            return None  
        except Exception as e:
            print(str(e)) 
            self.db_session.rollback()  
            return None

    def deleteClient(self, clientId):
        try:
            client = self.db_session.query(Client).filter_by(id=clientId).first()  
            if client:
                self.db_session.delete(client)  
                self.db_session.commit() 
                return True
            return None  
        except Exception as e:
            print(str(e))  
            self.db_session.rollback()  
            return None     
           
    # def clientRegister(self, username, email, password, first_name, last_name):
    #     try:
    #         client= Client(
    #         username=username,
    #         email=email,
    #         password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) ,
    #         first_name=first_name,
    #         last_name=last_name,
    #         bots=[],
    #         is_active=True,
    #         )
    #         client.save()
    #         return client
    #     except Exception as e: 
    #         print(str(e))
    #         return None

    # def clientLogin(self, email, password):
    #     try:
    #         client = Client.objects.get(email=email)
    #         if bcrypt.checkpw(password.encode('utf-8'), client.password.encode('utf-8') ):
    #             return True
    #         else:
    #             return False
    #     except Client.DoesNotExist:
    #         return None
    
    # def fetchClients(self):
    #     clients = Client.objects.all()
    #     return [client.to_json() for client in clients]
    
    # def returnClient(self, username):
    #     try:
    #         client = Client.objects.get(username=username)
    #         return client
    #     except Client.DoesNotExist:
    #         return None

    # def returnTokenInfo(self, username):
    #     try:
    #         client = Client.objects.get(username=username)
    #         return f"Allocated tokens: {client.tkns_remaining + client.tkns_used}",f"Remaining tokens: {client.tkns_remaining}", f"tokens used: {client.tkns_used}"
    #     except Client.DoesNotExist:
    #         return None
        
    # def updateClientBotToken(self, username, bot_id, addition):
    #     try:
    #         client = Client.objects.get(username=username)
    #         for bot in client.bots:
    #             if bot.id == bot_id:
    #                 bot.tkns_remaining += addition 
    #                 client.save() 
    #                 return True
    #         return None
    #     except Client.DoesNotExist:
    #         return None        
    
    # def addBot(self, user_id, bot_name, bot_id, tkns_remaining, tkns_used):
    #     try:
    #         client = Client.objects.get(id=user_id)
    #         new_bot = ClientBot(
    #             id=bot_id,
    #             name=bot_name,
    #             tkns_remaining=tkns_remaining,
    #             tkns_used=tkns_used
    #         )
    #         client.bots.append(new_bot)
    #         client.save()
    #         return True
    #     except Client.DoesNotExist:
    #         return None 
    
    # def deleteClientBot(self, user_id, bot_id):
    #     try:
    #         client = Client.objects.get(id=user_id)
    #         client.bots = [bot for bot in client.bots if bot.id != bot_id]
    #         client.save()
    #         return True
    #     except Client.DoesNotExist:
    #         return None          

    
    # def deleteClient(self, clientId):
    #     try:
    #         client = Client.objects.get(id=clientId)
    #         client.delete()
    #         return True
    #     except Client.DoesNotExist:
    #         return None          
