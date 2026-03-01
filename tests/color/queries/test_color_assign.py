import pytest


@pytest.mark.asyncio
class TestListColorAssigns:
    """Тесты для API получения списка назначений цветов"""

    async def test_list_color_assigns_200_empty(self, authorized_client):
        """Получение пустого списка назначений"""
        response = await authorized_client.get("/color-assign/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    async def test_list_color_assigns_200_with_data(self, authorized_client):
        """Получение списка с назначениями"""
        # Создаем цвета
        await authorized_client.post("/color/", json={"name": "цвет1"})
        await authorized_client.post("/color/", json={"name": "цвет2"})

        # Создаем назначения
        await authorized_client.post(
            "/color-assign/",
            json={"key": "key1", "color": "цвет1"},
        )
        await authorized_client.post(
            "/color-assign/",
            json={"key": "key2", "color": "цвет2"},
        )

        response = await authorized_client.get("/color-assign/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_list_color_assigns_filter_by_color(self, authorized_client):
        """Фильтрация назначений по цвету"""
        # Создаем цвета
        await authorized_client.post("/color/", json={"name": "красный"})
        await authorized_client.post("/color/", json={"name": "синий"})

        # Создаем назначения с разными цветами
        await authorized_client.post(
            "/color-assign/",
            json={"key": "key1", "color": "красный"},
        )
        await authorized_client.post(
            "/color-assign/",
            json={"key": "key2", "color": "красный"},
        )
        await authorized_client.post(
            "/color-assign/",
            json={"key": "key3", "color": "синий"},
        )

        # Фильтруем по цвету "красный"
        response = await authorized_client.get(
            "/color-assign/",
            params={"color": "красный"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["color"] == "красный" for item in data)

        # Фильтруем по цвету "синий"
        response = await authorized_client.get(
            "/color-assign/",
            params={"color": "синий"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["color"] == "синий"


@pytest.mark.asyncio
class TestGetColorAssign:
    """Тесты для API получения назначения по ID"""

    async def test_get_color_assign_200(self, authorized_client):
        """Успешное получение назначения"""
        # Создаем цвет и назначение
        await authorized_client.post(
            "/color/",
            json={"name": "нужный_цвет"},
        )
        create_response = await authorized_client.post(
            "/color-assign/",
            json={"key": "target_key", "color": "нужный_цвет"},
        )
        assign_id = create_response.json()["id"]

        # Получаем назначение
        response = await authorized_client.get(f"/color-assign/{assign_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == assign_id
        assert data["key"] == "target_key"
        assert data["color"] == "нужный_цвет"

    async def test_get_color_assign_404_not_found(self, authorized_client):
        """Получение несуществующего назначения возвращает 404"""
        response = await authorized_client.get("/color-assign/99999")
        assert response.status_code == 404
        assert "не найдено" in response.json()["message"]
