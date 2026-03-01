import pytest


@pytest.mark.asyncio
class TestCreateColor:
    """Тесты для API создания цвета"""

    async def test_create_color_200(self, authorized_client):
        """Успешное создание цвета"""
        response = await authorized_client.post(
            "/color/",
            json={"name": "красный"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "красный"

    async def test_create_color_409_already_exists(self, authorized_client):
        """Создание цвета с существующим именем возвращает 409"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "синий"},
        )
        # Пытаемся создать еще раз
        response = await authorized_client.post(
            "/color/",
            json={"name": "синий"},
        )
        assert response.status_code == 409
        assert "уже существует" in response.json()["message"]

    async def test_create_color_422_empty_name(self, authorized_client):
        """Создание цвета с пустым именем возвращает 422"""
        response = await authorized_client.post(
            "/color/",
            json={"name": ""},
        )
        assert response.status_code == 422

    async def test_create_color_422_name_too_long(self, authorized_client):
        """Создание цвета с именем длиннее 50 символов возвращает 422"""
        response = await authorized_client.post(
            "/color/",
            json={"name": "a" * 51},
        )
        assert response.status_code == 422

    async def test_create_color_401_unauthorized(self, client):
        """Создание цвета без авторизации возвращает 401"""
        response = await client.post(
            "/color/",
            json={"name": "зеленый"},
        )
        assert response.status_code == 401
