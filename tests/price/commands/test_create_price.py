import pytest


@pytest.mark.asyncio
class TestCreatePrice:
    """Тесты для API создания прайса"""

    async def test_create_price_200(self, authorized_client):
        """Успешное создание прайса"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["category"] == "электроника"
        assert data["data"]["supplier"] == "поставщик1"
        assert data["data"]["region"] == "москва"
        assert data["data"]["price_text"] == "Текст прайса"
        assert "id" in data["data"]

    async def test_create_price_creates_category_if_not_exists(self, authorized_client):
        """Создание прайса автоматически создает категорию если её нет"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "НоваяКатегория",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["category"] == "новаякатегория"

    async def test_create_price_creates_supplier_if_not_exists(self, authorized_client):
        """Создание прайса автоматически создает поставщика если его нет"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "НовыйПоставщик",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["supplier"] == "новыйпоставщик"

    async def test_create_price_creates_region_if_not_exists(self, authorized_client):
        """Создание прайса автоматически создает регион если его нет"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "НовыйРегион",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["region"] == "новыйрегион"

    async def test_create_price_409_already_exists(self, authorized_client):
        """Создание прайса с существующей комбинацией возвращает 409"""
        # Создаем прайс
        await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса 1",
            },
        )
        # Пытаемся создать еще раз с той же комбинацией
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса 2",
            },
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False
        assert "уже существует" in json_response["error"]["message"]

    async def test_create_price_422_empty_category(self, authorized_client):
        """Создание прайса с пустой категорией возвращает 422"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 422

    async def test_create_price_422_empty_supplier(self, authorized_client):
        """Создание прайса с пустым поставщиком возвращает 422"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 422

    async def test_create_price_422_empty_region(self, authorized_client):
        """Создание прайса с пустым регионом возвращает 422"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 422

    async def test_create_price_422_empty_price_text(self, authorized_client):
        """Создание прайса с пустым текстом возвращает 422"""
        response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "",
            },
        )
        assert response.status_code == 422

    async def test_create_price_401_unauthorized(self, client):
        """Создание прайса без авторизации возвращает 401"""
        response = await client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст прайса",
            },
        )
        assert response.status_code == 401

    async def test_create_price_different_combinations(self, authorized_client):
        """Создание прайсов с разными комбинациями category/supplier/region"""
        # Создаем первый прайс
        response1 = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст 1",
            },
        )
        assert response1.status_code == 200

        # Создаем второй прайс с другим регионом
        response2 = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "СПб",
                "price_text": "Текст 2",
            },
        )
        assert response2.status_code == 200

        # Создаем третий прайс с другим поставщиком
        response3 = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик2",
                "region": "Москва",
                "price_text": "Текст 3",
            },
        )
        assert response3.status_code == 200

        # Создаем четвертый прайс с другой категорией
        response4 = await authorized_client.post(
            "/price/",
            json={
                "category": "Одежда",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст 4",
            },
        )
        assert response4.status_code == 200
