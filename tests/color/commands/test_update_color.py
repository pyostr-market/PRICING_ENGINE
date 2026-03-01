import pytest


@pytest.mark.asyncio
class TestUpdateColor:
    """Тесты для API обновления цвета"""

    async def test_update_color_200(self, authorized_client):
        """Успешное обновление цвета"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "старый"},
        )
        # Обновляем
        response = await authorized_client.put(
            "/color/старый",
            json={"name": "новый"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "новый"

    async def test_update_color_404_not_found(self, authorized_client):
        """Обновление несуществующего цвета возвращает 404"""
        response = await authorized_client.put(
            "/color/несуществующий",
            json={"name": "новый"},
        )
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]

    async def test_update_color_409_name_already_exists(self, authorized_client):
        """Обновление цвета на существующее имя возвращает 409"""
        # Создаем два цвета
        await authorized_client.post(
            "/color/",
            json={"name": "цвет1"},
        )
        await authorized_client.post(
            "/color/",
            json={"name": "цвет2"},
        )
        # Пытаемся переименовать цвет1 в цвет2
        response = await authorized_client.put(
            "/color/цвет1",
            json={"name": "цвет2"},
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False
        assert "уже существует" in json_response["error"]["message"]

    async def test_update_color_422_empty_name(self, authorized_client):
        """Обновление цвета с пустым именем возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "тест"},
        )
        response = await authorized_client.put(
            "/color/тест",
            json={"name": ""},
        )
        assert response.status_code == 422

    async def test_update_color_422_name_too_long(self, authorized_client):
        """Обновление цвета с именем длиннее 50 символов возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "тест"},
        )
        response = await authorized_client.put(
            "/color/тест",
            json={"name": "a" * 51},
        )
        assert response.status_code == 422

    async def test_update_color_401_unauthorized(self, client):
        """Обновление цвета без авторизации возвращает 401"""
        response = await client.put(
            "/color/тест",
            json={"name": "новый"},
        )
        assert response.status_code == 401
