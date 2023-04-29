from django.core.management import BaseCommand
from todolist import settings
from uuid import uuid4
from todolist.bot.models import TgUser
from todolist.bot.tg.client import TgClient
from todolist.bot.tg.schemas import Message
from todolist.goals.models import Goal, GoalCategory

storage = {
    'command': '',
    'list_categories': '',
    'category': '',
    'goal_title': '',
    'permission': 'no',
}


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if not tg_user.user:
            # Пользователь телеги НЕ привязан к пользователю приложения
            self.tg_client.send_message(msg.chat.id, 'Подтвердите, пожалуйста, свой аккаунт')
            verification_code = str(uuid4())
            tg_user.verification_code = verification_code
            tg_user.save(update_fields=['verification_code'])
            self.tg_client.send_message(msg.chat.id, f'Verification code: {verification_code}')
        else:
            # Пользователь телеги привязан к пользователю приложения
            self.handle_authorized_user(tg_user, msg)

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        if msg.text.startswith('/'):
            self.handle_command(tg_user, msg.text)
        else:
            if storage['permission'] == 'yes':
                storage['goal_title'] = msg.text
                self.create_goal_cat(tg_user, msg.text, storage['category'])
                return
            if storage['command'] == '/create':
                # сравниваем со списком категорий
                if msg.text in storage['list_categories']:
                    storage['category'] = msg.text
                    self.tg_client.send_message(msg.chat.id,
                                                f"Выбрана категория {storage['category']}. Введите название цели")
                    storage['goal_title'] = msg.text
                    storage['permission'] = 'yes'
                    return
                else:
                    self.tg_client.send_message(msg.chat.id, 'Нет такой категории. Попробуйте еще')
                    return
            if storage['command'] == '/cancel':
                self.tg_client.send_message(msg.chat.id, 'Операция отклонена')
                storage['command'] = ''
            else:
                self.tg_client.send_message(msg.chat.id, 'Введите команду')

    def handle_command(self, tg_user: TgUser, command: str):
        match command:
            case '/goals':
                goals = Goal.objects.select_related('user').filter(
                    category__board__participants__user=tg_user.user, category__is_deleted=False
                ).exclude(status=Goal.Status.archived)
                if not goals:
                    self.tg_client.send_message(tg_user.chat_id, 'No goals')
                else:
                    resp = '\n'.join([goal.title for goal in goals])
                    self.tg_client.send_message(tg_user.chat_id, resp)
                    return self.tg_client.get_updates()
            case '/create':
                self.tg_client.send_message(tg_user.chat_id, 'Выберете категорию, для которой нужно создать цель')
                categories = GoalCategory.objects.select_related('user').filter(
                    board__participants__user=tg_user.user, is_deleted=False
                )
                if not categories:
                    self.tg_client.send_message(tg_user.chat_id, 'No category')
                else:
                    resp = [category.title for category in categories]
                    storage['list_categories'] = resp
                    resp = '\n'.join([category.title for category in categories])
                    self.tg_client.send_message(tg_user.chat_id, resp)
                    storage['command'] = '/create'
            case '/cancel':
                storage['command'] = '/cancel'
                self.tg_client.send_message(tg_user.chat_id, 'Операция отклонена')
                return storage
            case _:
                self.tg_client.send_message(tg_user.chat_id, 'Неизвестная команда')
                self.handle(tg_user, None)

    def create_goal_cat(self, tg_user, title, category):
        categories = GoalCategory.objects.select_related('user').filter(
            board__participants__user=tg_user.user, title=category, is_deleted=False
        )
        category = [category for category in categories]
        goal = Goal.objects.create(user=tg_user.user, title=title, category=category[0])
        self.tg_client.send_message(tg_user.chat_id, 'Цель успешно создана\n'
                                    + f"http://158.160.57.32/boards/{category[0].board.id}/goals?goal={goal.id}")
        # обнуляем словарь
        storage['command'] = ''
        storage['list_categories'] = ''
        storage['category'] = ''
        storage['goal_title'] = ''
        storage['permission'] = 'no'
