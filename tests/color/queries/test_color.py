import pytest


@pytest.mark.asyncio
class TestListColors:
    """Тесты для API получения списка цветов"""

    async def test_list_colors_200_empty(self, authorized_client):
        """Получение пустого списка цветов"""
        response = await authorized_client.get("/color/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["items"] == []
        assert data["data"]["total"] == 0

    async def test_list_colors_200_with_data(self, authorized_client):
        """Получение списка с цветами"""
        # Создаем несколько цветов
        await authorized_client.post("/color/", json={"name": "цвет1"})
        await authorized_client.post("/color/", json={"name": "цвет2"})
        await authorized_client.post("/color/", json={"name": "цвет3"})

        response = await authorized_client.get("/color/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        items = data["data"]["items"]
        total = data["data"]["total"]
        assert len(items) == 3
        assert total == 3
        names = [item["name"] for item in items]
        assert "цвет1" in names
        assert "цвет2" in names
        assert "цвет3" in names

    async def test_list_colors_sorted(self, authorized_client):
        """Цвета возвращаются отсортированными по имени"""
        await authorized_client.post("/color/", json={"name": "черный"})
        await authorized_client.post("/color/", json={"name": "белый"})
        await authorized_client.post("/color/", json={"name": "алый"})

        response = await authorized_client.get("/color/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        items = data["data"]["items"]
        names = [item["name"] for item in items]
        assert names == sorted(names)

    async def test_list_colors_pagination(self, authorized_client):
        """Тест пагинации списка цветов"""
        # Создаем 15 цветов
        for i in range(15):
            await authorized_client.post("/color/", json={"name": f"цвет{i}"})

        # Получаем первые 10
        response = await authorized_client.get("/color/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["items"]) == 10
        assert data["data"]["total"] == 15

        # Получаем следующие 5
        response = await authorized_client.get("/color/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 5
        assert data["data"]["total"] == 15


@pytest.mark.asyncio
class TestGetColor:
    """Тесты для API получения цвета по имени"""

    async def test_get_color_200(self, authorized_client):
        """Успешное получение цвета"""
        # Создаем цвет
        await authorized_client.post(
            "/color/",
            json={"name": "искомый_цвет"},
        )
        # Получаем
        response = await authorized_client.get("/color/искомый_цвет")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "искомый_цвет"

    async def test_get_color_404_not_found(self, authorized_client):
        """Получение несуществующего цвета возвращает 404"""
        response = await authorized_client.get("/color/несуществующий")
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]
