import pytest


@pytest.mark.asyncio
class TestUpdateColorAssign:
    """Тесты для API обновления назначения цвета"""

    async def test_update_color_assign_200(self, authorized_client):
        """Успешное обновление назначения"""
        # Создаем цвет и назначение
        await authorized_client.post(
            "/color/",
            json={"name": "старый_цвет"},
        )
        await authorized_client.post(
            "/color/",
            json={"name": "новый_цвет"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "old_key", "color": "старый_цвет"},
        )
        assign_id = create_response.json()["data"]["id"]

        # Обновляем
        response = await authorized_client.put(
            f"/color-assign/{assign_id}",
            json={"key": "new_key", "color": "новый_цвет"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["key"] == "new_key"
        assert data["data"]["color"] == "новый_цвет"
        assert data["data"]["id"] == assign_id

    async def test_update_color_assign_200_partial_update(self, authorized_client):
        """Частичное обновление назначения (только ключ или только цвет)"""
        await authorized_client.post(
            "/color/",
            json={"name": "цвет1"},
        )
        await authorized_client.post(
            "/color/",
            json={"name": "цвет2"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "key1", "color": "цвет1"},
        )
        assign_id = create_response.json()["data"]["id"]

        # Обновляем только цвет
        response = await authorized_client.put(
            f"/color-assign/{assign_id}",
            json={"color": "цвет2"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["key"] == "key1"
        assert data["data"]["color"] == "цвет2"

    async def test_update_color_assign_404_not_found(self, authorized_client):
        """Обновление несуществующего назначения возвращает 404"""
        response = await authorized_client.put(
            "/color-assign/99999",
            json={"key": "new_key", "color": "красный"},
        )
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найдено" in json_response["error"]["message"]

    async def test_update_color_assign_409_invalid_color(self, authorized_client):
        """Обновление с несуществующим цветом возвращает ошибку"""
        await authorized_client.post(
            "/color/",
            json={"name": "существующий"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "test_key", "color": "существующий"},
        )
        assign_id = create_response.json()["data"]["id"]

        response = await authorized_client.put(
            f"/color-assign/{assign_id}",
            json={"color": "несуществующий"},
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False

    async def test_update_color_assign_422_empty_key(self, authorized_client):
        """Обновление с пустым ключом возвращает 422"""
        await authorized_client.post(
            "/color/",
            json={"name": "тест"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "test", "color": "тест"},
        )
        assign_id = create_response.json()["data"]["id"]

        response = await authorized_client.put(
            f"/color-assign/{assign_id}",
            json={"key": ""},
        )
        assert response.status_code == 422

    async def test_update_color_assign_401_unauthorized(self, client):
        """Обновление без авторизации возвращает 401"""
        response = await client.put(
            "/color-assign/1",
            json={"key": "new_key", "color": "красный"},
        )
        assert response.status_code == 401
