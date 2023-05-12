from typing import Callable
from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError

from todolist.goals.models import BoardParticipant, Board


@pytest.fixture()
def category_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestCategoryCreateView:
    url = reverse('todolist.goals:create-category')

    def test_auth_required(self, client, category_create_data):
        """
        Неавторизованный пользователь при создании категории получит ошибку авторизации
        """
        response = client.post(self.url, data=category_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.owner,
    ], ids=['writer', 'owner'])
    def test_goal_create(self, client, user_factory, board, board_participant_factory, role, category_create_data):
        """
        Пользователь с правами владельца или редактора доски может создать категорию
        """
        user = user_factory.create()
        board_participant_factory.create(user=user, board=board, role=role)
        client.force_login(user)

        response = client.post(self.url, data=category_create_data(board=board.id), )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.owner,
    ], ids=['writer', 'owner'])
    def test_goal_create_with_deleted_board(self, client, user_factory, board, board_participant_factory, role,
                                            category_create_data):
        """
        Пользователь с правами владельца или редактора доски не может создать удаленную категорию
        """
        user = user_factory.create()
        board.is_deleted = True
        board_participant_factory.create(user=user, board=board, role=role)
        client.force_login(user)
        response = client.post(self.url, data=category_create_data(board=board.id), )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serialize_category_response(is_deleted=False)

    def test_goal_create_reader(self, client, user_factory, board, board_participant_factory,
                                category_create_data):
        """
        Пользователь с правами читателя доски не может создавать категорию
        """
        user = user_factory.create()
        board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.reader)
        client.force_login(user)
        response = client.post(self.url, data=category_create_data(board=board.id), )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def _serialize_category_response(self, **kwargs) -> dict:
        data = {
            'id': ANY,
            'created': ANY,
            'updated': ANY,
            'title': ANY,
            'is_deleted': False,
            'board': ANY
        }
        data |= kwargs
        return data
