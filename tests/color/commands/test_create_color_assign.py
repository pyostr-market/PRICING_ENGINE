import pytest


@pytest.mark.asyncio
class TestCreateColorAssign:
    """Тесты для API создания назначения цвета"""

    async def test_create_color_assign_200(self, authorized_client):
        """Успешное создание назначения цвета"""
        # Сначала создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "красный"},
        )
        # Создаем назначение
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "product_1", "color": "красный"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["key"] == "product_1"
        assert data["data"]["color"] == "красный"
        assert "id" in data["data"]

    async def test_create_color_assign_409_already_exists(self, authorized_client):
        """Создание дубликата назначения возвращает 409"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "синий"},
        )
        # Создаем назначение
        await authorized_client.post(
            "/color-assign/",
            json={"key": "product_2", "color": "синий"},
        )
        # Пытаемся создать дубликат
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "product_2", "color": "синий"},
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False
        assert "уже существует" in json_response["error"]["message"]

    async def test_create_color_assign_409_invalid_color(self, authorized_client):
        """Создание назначения с несуществующим цветом возвращает ошибку"""
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "product_3", "color": "несуществующий_цвет"},
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False
        assert "не существует" in json_response["error"]["message"]

    async def test_create_color_assign_422_empty_key(self, authorized_client):
        """Создание назначения с пустым ключом возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "зеленый"},
        )
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "", "color": "зеленый"},
        )
        assert response.status_code == 422

    async def test_create_color_assign_422_key_too_long(self, authorized_client):
        """Создание назначения с ключом длиннее 50 символов возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "желтый"},
        )
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "a" * 51, "color": "желтый"},
        )
        assert response.status_code == 422

    async def test_create_color_assign_422_color_too_long(self, authorized_client):
        """Создание назначения с цветом длиннее 50 символов возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "a" * 50},
        )
        response = await authorized_client.post(
            "/color-assign/",
            json={"key": "test", "color": "a" * 51},
        )
        assert response.status_code == 422

    async def test_create_color_assign_401_unauthorized(self, client):
        """Создание назначения без авторизации возвращает 401"""
        response = await client.post(
            "/color-assign/",
            json={"key": "test", "color": "красный"},
        )
        assert response.status_code == 401
