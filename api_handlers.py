# api_handlers.py
import asyncio
import async_timeout
import aiohttp
from typing import AsyncIterator
from datetime import datetime



class APIHandler:
    def __init__(self, dialog_url: str, bron_url: str, sogl_url: str, timeout: int = 40):
        self.dialog_url = dialog_url
        self.bron_url = bron_url
        self.sogl_url = sogl_url
        self.timeout = timeout


    async def run_dialog(self, user_id: str, user_question: str) -> AsyncIterator[str]:
        """
        Асинхронная функция для общения с ChatGPT.

        Args:
            user_id (str): Идентификатор пользователя.
            user_question (str): Вопрос пользователя.

        Yields:
            str: Часть ответа ChatGPT.
        """
        payload = {"user_id": user_id, "text": user_question}
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self.timeout):
                async with session.post(self.dialog_url, json=payload) as resp:
                    if resp.status != 200:
                        raise ValueError(f"Код от сервера если не ответил {resp.status}")

                    async with async_timeout.timeout(self.timeout):
                        async for chunk in resp.content.iter_chunked(128):
                            yield chunk.decode()


    async def run_bron(self, user_id: str, user_question: str) -> AsyncIterator[str]:
        """
        Асинхронная функция для бронирования.

        Args:
            user_id (str): Идентификатор пользователя.
            user_question (str): Вопрос пользователя.

        Yields:
            str: Часть ответа бронирования.
        """
        payload = {"user_id": user_id, "text": user_question}
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self.timeout):
                async with session.post(self.bron_url, json=payload) as resp:
                    if resp.status != 200:
                        raise ValueError(f"Код от сервера если не ответил {resp.status}")

                    async with async_timeout.timeout(self.timeout):
                        async for chunk in resp.content.iter_chunked(128):
                            yield chunk.decode()


    async def run_sogl(self, user_id: str, user_question: str) -> AsyncIterator[str]:
        """
        Асинхронная функция для бронирования.

        Args:
            user_id (str): Идентификатор пользователя.
            user_question (str): Вопрос пользователя.

        Yields:
            str: Часть ответа бронирования.
        """
        payload = {"user_id": user_id, "text": user_question}
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self.timeout):
                async with session.post(self.sogl_url, json=payload) as resp:
                    if resp.status != 200:
                        raise ValueError(f"Код от сервера если не ответил {resp.status}")

                    async with async_timeout.timeout(self.timeout):
                        async for chunk in resp.content.iter_chunked(128):
                            yield chunk.decode()




    async def handle_dialog(self, update, context, user_id, user_question):
        try:
            async with async_timeout.timeout(60):
                
                dialog = ''
                message = None  # Инициализируем message как None
                async for chunk in self.run_dialog(user_id, user_question):
                    if chunk is not None:  
                        dialog += chunk

                        if message == None:
                            message = await context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=dialog
                            )
                        else:
                            await context.bot.edit_message_text(
                                chat_id=update.effective_chat.id,
                                message_id=message.message_id,
                                text=dialog 
                                )

        except asyncio.TimeoutError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Превышено время ожидания ответа от сервера. Пожалуйста, попробуйте еще раз.'
            )

    async def handle_bron(self, update, context, user_id, user_question):
        try:
            dialog = ''
            message = None  # Инициализируем message как None
            from hotels_tg_bot import simple_b
            async for chunk in self.run_bron(user_id, user_question):      
                if chunk is not None:                     
                    dialog += chunk
                    if message == None:
                        message = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=dialog,
                            reply_markup=await simple_b(update, context)
                        )
                    else:    
                        await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=message.message_id,
                        text=dialog,
                        reply_markup=await simple_b(update, context)
                    )

        except asyncio.TimeoutError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Превышено время ожидания ответа от сервера. Пожалуйста, попробуйте еще раз.'
            )
    

    async def handle_sogl(self, update, context, user_id, user_question):
        try:
            
            dialog = ''
            message = None  # Инициализируем message как None
            from hotels_tg_bot import simple_b
            async for chunk in self.run_sogl(user_id, user_question):      
                if chunk is not None:                     
                    dialog += chunk
                    if message == None:
                        message = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=dialog,
                            reply_markup=await simple_b(update, context)
                        )
                    else:    
                        await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=message.message_id,
                        text=dialog,
                        reply_markup=await simple_b(update, context)
                    )

        except asyncio.TimeoutError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Превышено время ожидания ответа от сервера. Пожалуйста, попробуйте еще раз.'
            )
    