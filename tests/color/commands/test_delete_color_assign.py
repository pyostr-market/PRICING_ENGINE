import pytest


@pytest.mark.asyncio
class TestDeleteColorAssign:
    """Тесты для API удаления назначения цвета"""

    async def test_delete_color_assign_200(self, authorized_client):
        """Успешное удаление назначения"""
        # Создаем цвет и назначение
        await authorized_client.post(
            "/color/",
            json={"name": "цвет_для_удаления"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "delete_key", "color": "цвет_для_удаления"},
        )
        assign_id = create_response.json()["id"]

        # Удаляем
        response = await authorized_client.delete(
            f"/color-assign/{assign_id}",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] is True

    async def test_delete_color_assign_404_not_found(self, authorized_client):
        """Удаление несуществующего назначения возвращает 404"""
        response = await authorized_client.delete(
            "/color-assign/99999",
        )
        assert response.status_code == 404
        assert "не найдено" in response.json()["message"]

    async def test_delete_color_assign_401_unauthorized(self, client):
        """Удаление без авторизации возвращает 401"""
        response = await client.delete(
            "/color-assign/1",
        )
        assert response.status_code == 401

    async def test_delete_color_assign_verify_removed(self, authorized_client):
        """Проверка, что назначение действительно удалено из БД"""
        # Создаем цвет и назначение
        await authorized_client.post(
            "/color/",
            json={"name": "проверочный_цвет"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "verify_key", "color": "проверочный_цвет"},
        )
        assign_id = create_response.json()["id"]

        # Проверяем, что назначение существует
        get_before = await authorized_client.get(f"/color-assign/{assign_id}")
        assert get_before.status_code == 200

        # Удаляем
        await authorized_client.delete(f"/color-assign/{assign_id}")

        # Проверяем, что назначение удалено
        get_after = await authorized_client.get(f"/color-assign/{assign_id}")
        assert get_after.status_code == 404
