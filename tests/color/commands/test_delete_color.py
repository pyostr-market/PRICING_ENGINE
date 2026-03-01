import pytest


@pytest.mark.asyncio
class TestDeleteColor:
    """Тесты для API удаления цвета"""

    async def test_delete_color_200(self, authorized_client):
        """Успешное удаление цвета"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "удаляемый"},
        )
        # Удаляем
        response = await authorized_client.delete(
            "/color/удаляемый",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["deleted"] is True

    async def test_delete_color_404_not_found(self, authorized_client):
        """Удаление несуществующего цвета возвращает 404"""
        response = await authorized_client.delete(
            "/color/несуществующий",
        )
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]

    async def test_delete_color_401_unauthorized(self, client):
        """Удаление цвета без авторизации возвращает 401"""
        response = await client.delete(
            "/color/тест",
        )
        assert response.status_code == 401

    async def test_delete_color_cascade(self, authorized_client):
        """Удаление цвета каскадно удаляет связанные назначения"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "цвет_для_каскада"},
        )
        # Создаем назначение
        create_assign_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "test_key", "color": "цвет_для_каскада"},
        )
        assert create_assign_response.status_code == 200
        assign_id = create_assign_response.json()["data"]["id"]

        # Проверяем, что назначение существует
        get_response = await authorized_client.get(f"/color-assign/{assign_id}")
        assert get_response.status_code == 200

        # Удаляем цвет
        delete_response = await authorized_client.delete(
            "/color/цвет_для_каскада",
        )
        assert delete_response.status_code == 200

        # Проверяем, что назначение удалено (каскадно)
        get_after_delete = await authorized_client.get(f"/color-assign/{assign_id}")
        assert get_after_delete.status_code == 404
