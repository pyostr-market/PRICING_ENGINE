import pytest


@pytest.mark.asyncio
class TestUpdatePrice:
    """Тесты для API обновления прайса"""

    async def test_update_price_200(self, authorized_client):
        """Успешное обновление прайса"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Старый текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Обновляем
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Новый текст",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["price_text"] == "Новый текст"

    async def test_update_price_200_partial_update(self, authorized_client):
        """Частичное обновление прайса (только price_text)"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Старый текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Обновляем только текст
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "price_text": "Обновленный текст",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["price_text"] == "Обновленный текст"
        assert data["data"]["category"] == "электроника"
        assert data["data"]["supplier"] == "поставщик1"
        assert data["data"]["region"] == "москва"

    async def test_update_price_200_creates_new_category(self, authorized_client):
        """Обновление прайса создает новую категорию если её нет"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Обновляем с новой категорией
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "category": "НоваяКатегория",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["category"] == "новаякатегория"

    async def test_update_price_200_creates_new_supplier(self, authorized_client):
        """Обновление прайса создает нового поставщика если его нет"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Обновляем с новым поставщиком
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "supplier": "НовыйПоставщик",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["supplier"] == "новыйпоставщик"

    async def test_update_price_200_creates_new_region(self, authorized_client):
        """Обновление прайса создает новый регион если его нет"""
        # Создаем прайс
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Обновляем с новым регионом
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "region": "НовыйРегион",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["region"] == "новыйрегион"

    async def test_update_price_404_not_found(self, authorized_client):
        """Обновление несуществующего прайса возвращает 404"""
        response = await authorized_client.put(
            "/price/99999",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]

    async def test_update_price_409_already_exists(self, authorized_client):
        """Обновление прайса на существующую комбинацию возвращает 409"""
        # Создаем первый прайс
        await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст 1",
            },
        )
        # Создаем второй прайс с другой комбинацией
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Одежда",
                "supplier": "Поставщик2",
                "region": "СПб",
                "price_text": "Текст 2",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Пытаемся обновить второй прайс на комбинацию первого
        response = await authorized_client.put(
            f"/price/{price_id}",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
            },
        )
        assert response.status_code == 409
        json_response = response.json()
        assert json_response["success"] is False
        assert "уже существует" in json_response["error"]["message"]

    async def test_update_price_422_empty_category(self, authorized_client):
        """Обновление прайса с пустой категорией возвращает 422"""
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        response = await authorized_client.put(
            f"/price/{price_id}",
            json={"category": ""},
        )
        assert response.status_code == 422

    async def test_update_price_422_empty_supplier(self, authorized_client):
        """Обновление прайса с пустым поставщиком возвращает 422"""
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        response = await authorized_client.put(
            f"/price/{price_id}",
            json={"supplier": ""},
        )
        assert response.status_code == 422

    async def test_update_price_422_empty_region(self, authorized_client):
        """Обновление прайса с пустым регионом возвращает 422"""
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        price_id = create_response.json()["data"]["id"]

        response = await authorized_client.put(
            f"/price/{price_id}",
            json={"region": ""},
        )
        assert response.status_code == 422

    async def test_update_price_401_unauthorized(self, client):
        """Обновление прайса без авторизации возвращает 401"""
        response = await client.put(
            "/price/1",
            json={
                "category": "Электроника",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст",
            },
        )
        assert response.status_code == 401
