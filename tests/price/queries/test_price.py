import pytest


@pytest.mark.asyncio
class TestListPrices:
    """Тесты для API получения списка прайсов"""

    async def test_list_prices_200_empty(self, authorized_client):
        """Получение пустого списка прайсов"""
        response = await authorized_client.get("/price/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["items"] == []
        assert data["data"]["total"] == 0

    async def test_list_prices_200_with_data(self, authorized_client):
        """Получение списка с прайсами"""
        # Создаем несколько прайсов
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "Регион1",
                "price_text": "Текст 1",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "Поставщик2",
                "region": "Регион2",
                "price_text": "Текст 2",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория3",
                "supplier": "Поставщик3",
                "region": "Регион3",
                "price_text": "Текст 3",
            },
        )

        response = await authorized_client.get("/price/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        items = data["data"]["items"]
        total = data["data"]["total"]
        assert len(items) == 3
        assert total == 3

    async def test_list_prices_sorted_by_id(self, authorized_client):
        """Прайсы возвращаются отсортированными по ID"""
        # Создаем прайсы
        response1 = await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "Регион1",
                "price_text": "Текст 1",
            },
        )
        response2 = await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "Поставщик2",
                "region": "Регион2",
                "price_text": "Текст 2",
            },
        )
        response3 = await authorized_client.post(
            "/price/",
            json={
                "category": "Категория3",
                "supplier": "Поставщик3",
                "region": "Регион3",
                "price_text": "Текст 3",
            },
        )

        response = await authorized_client.get("/price/")
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        ids = [item["id"] for item in items]
        assert ids == sorted(ids)

    async def test_list_prices_filter_by_category(self, authorized_client):
        """Фильтрация прайсов по категории"""
        # Создаем прайсы с одинаковой категорией
        await authorized_client.post(
            "/price/",
            json={
                "category": "ОбщаяКатегория",
                "supplier": "Поставщик1",
                "region": "Регион1",
                "price_text": "Текст 1",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "ОбщаяКатегория",
                "supplier": "Поставщик2",
                "region": "Регион2",
                "price_text": "Текст 2",
            },
        )
        # Создаем прайс с другой категорией
        await authorized_client.post(
            "/price/",
            json={
                "category": "ДругаяКатегория",
                "supplier": "Поставщик3",
                "region": "Регион3",
                "price_text": "Текст 3",
            },
        )

        response = await authorized_client.get("/price/?category=общаякатегория")
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        total = data["data"]["total"]
        assert len(items) == 2
        assert total == 2
        assert all(item["category"] == "общаякатегория" for item in items)

    async def test_list_prices_filter_by_supplier(self, authorized_client):
        """Фильтрация прайсов по поставщику"""
        # Создаем прайсы с одинаковым поставщиком
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "ОбщийПоставщик",
                "region": "Регион1",
                "price_text": "Текст 1",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "ОбщийПоставщик",
                "region": "Регион2",
                "price_text": "Текст 2",
            },
        )
        # Создаем прайс с другим поставщиком
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория3",
                "supplier": "ДругойПоставщик",
                "region": "Регион3",
                "price_text": "Текст 3",
            },
        )

        response = await authorized_client.get("/price/?supplier=общийпоставщик")
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        assert len(items) == 2
        assert all(item["supplier"] == "общийпоставщик" for item in items)

    async def test_list_prices_filter_by_region(self, authorized_client):
        """Фильтрация прайсов по региону"""
        # Создаем прайсы с одинаковым регионом
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "ОбщийРегион",
                "price_text": "Текст 1",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "Поставщик2",
                "region": "ОбщийРегион",
                "price_text": "Текст 2",
            },
        )
        # Создаем прайс с другим регионом
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория3",
                "supplier": "Поставщик3",
                "region": "ДругойРегион",
                "price_text": "Текст 3",
            },
        )

        response = await authorized_client.get("/price/?region=общийрегион")
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        assert len(items) == 2
        assert all(item["region"] == "общийрегион" for item in items)

    async def test_list_prices_combined_filters(self, authorized_client):
        """Комбинированная фильтрация прайсов"""
        # Создаем прайсы
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "Регион1",
                "price_text": "Текст 1",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "Регион2",
                "price_text": "Текст 2",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик2",
                "region": "Регион1",
                "price_text": "Текст 3",
            },
        )
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "Поставщик1",
                "region": "Регион1",
                "price_text": "Текст 4",
            },
        )

        # Фильтруем по категории и поставщику
        response = await authorized_client.get(
            "/price/?category=категория1&supplier=поставщик1"
        )
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        assert len(items) == 2

        # Фильтруем по категории и региону
        response = await authorized_client.get(
            "/price/?category=категория1&region=регион1"
        )
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        assert len(items) == 2

        # Фильтруем по всем трем параметрам
        response = await authorized_client.get(
            "/price/?category=категория1&supplier=поставщик1&region=регион1"
        )
        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        assert len(items) == 1
        assert items[0]["price_text"] == "Текст 1"

    async def test_list_prices_pagination(self, authorized_client):
        """Тест пагинации списка прайсов"""
        # Создаем 15 прайсов
        for i in range(15):
            await authorized_client.post(
                "/price/",
                json={
                    "category": f"Категория{i}",
                    "supplier": f"Поставщик{i}",
                    "region": f"Регион{i}",
                    "price_text": f"Текст {i}",
                },
            )

        # Получаем первые 10
        response = await authorized_client.get("/price/?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["items"]) == 10
        assert data["data"]["total"] == 15

        # Получаем следующие 5
        response = await authorized_client.get("/price/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 5
        assert data["data"]["total"] == 15


@pytest.mark.asyncio
class TestGetPrice:
    """Тесты для API получения прайса по ID"""

    async def test_get_price_200(self, authorized_client):
        """Успешное получение прайса"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Получаем
        response = await authorized_client.get(f"/price/{price_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == price_id
        assert data["data"]["category"] == "электроника"
        assert data["data"]["supplier"] == "поставщик1"
        assert data["data"]["region"] == "москва"
        assert data["data"]["price_text"] == "Текст прайса"

    async def test_get_price_404_not_found(self, authorized_client):
        """Получение несуществующего прайса возвращает 404"""
        response = await authorized_client.get("/price/99999")
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]

    async def test_get_price_401_unauthorized(self, client):
        """Получение прайса без авторизации возвращает 401"""
        response = await client.get("/price/1")
        assert response.status_code == 401
