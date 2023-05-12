import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.mark.django_db()
class TestCategoryRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, goal_category):
        self.url = self.get_url(goal_category.id)

    @staticmethod
    def get_url(category_pk: int) -> str:
        return reverse('todolist.goals:goal-category', kwargs={'pk': category_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может просматривать категории
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_category(self, auth_client, category_factory):
        """
        Авторизованный пользователь не может просматривать удаленные категории
        """
        category = category_factory.create()
        category.is_deleted = True
        category.save()

        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_category(self, client, user_factory):
        """
        Пользователь не может просматривать категории доски, участником которой он не является
        """
        user = user_factory.create()
        client.force_login(user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
class TestCategoryDestroyView:

    @pytest.fixture(autouse=True)
    def setup(self, goal_category):
        self.url = self.get_url(goal_category.id)

    @staticmethod
    def get_url(goal_category_pk: int) -> str:
        return reverse('todolist.goals:goal-category', kwargs={'pk': goal_category_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может удалить категорию
        """
        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_not_owner_failed_to_delete_category(self, client, user_factory, board, board_participant_factory):
        """
        Пользователь, являющийся с правами читателя, не может удалить категорию
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=BoardParticipant.Role.reader)
        client.force_login(another_user)

        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.owner,
    ], ids=['writer', 'owner'])
    def test_not_owner_can_to_delete_category(self, client, user_factory, board, board_participant_factory, role):
        """
        Пользователь, являющийся владельцем или редактором, может удалить категорию
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
