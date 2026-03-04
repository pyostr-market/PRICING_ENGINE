import pytest


@pytest.mark.asyncio
class TestDeletePrice:
    """Тесты для API удаления прайса"""

    async def test_delete_price_200(self, authorized_client):
        """Успешное удаление прайса"""
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

        # Удаляем
        response = await authorized_client.delete(f"/price/{price_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["deleted"] is True

    async def test_delete_price_404_not_found(self, authorized_client):
        """Удаление несуществующего прайса возвращает 404"""
        response = await authorized_client.delete("/price/99999")
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["success"] is False
        assert "не найден" in json_response["error"]["message"]

    async def test_delete_price_401_unauthorized(self, client):
        """Удаление прайса без авторизации возвращает 401"""
        response = await client.delete("/price/1")
        assert response.status_code == 401

    async def test_delete_price_cascade_category(self, authorized_client):
        """Удаление прайса каскадно не удаляет категорию (если она используется в другом прайсе)"""
        # Создаем категорию через первый прайс
        await authorized_client.post(
            "/price/",
            json={
                "category": "ОбщаяКатегория",
                "supplier": "Поставщик1",
                "region": "Москва",
                "price_text": "Текст 1",
            },
        )
        # Создаем второй прайс с той же категорией
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "ОбщаяКатегория",
                "supplier": "Поставщик2",
                "region": "СПб",
                "price_text": "Текст 2",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Удаляем второй прайс
        delete_response = await authorized_client.delete(f"/price/{price_id}")
        assert delete_response.status_code == 200

        # Первый прайс должен остаться
        get_response = await authorized_client.get("/price/?category=общаякатегория")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data["data"]["items"]) == 1

    async def test_delete_price_cascade_supplier(self, authorized_client):
        """Удаление прайса каскадно не удаляет поставщика (если он используется в другом прайсе)"""
        # Создаем первый прайс
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "ОбщийПоставщик",
                "region": "Москва",
                "price_text": "Текст 1",
            },
        )
        # Создаем второй прайс с тем же поставщиком
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "ОбщийПоставщик",
                "region": "СПб",
                "price_text": "Текст 2",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Удаляем второй прайс
        delete_response = await authorized_client.delete(f"/price/{price_id}")
        assert delete_response.status_code == 200

        # Первый прайс должен остаться
        get_response = await authorized_client.get("/price/?supplier=общийпоставщик")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data["data"]["items"]) == 1

    async def test_delete_price_cascade_region(self, authorized_client):
        """Удаление прайса каскадно не удаляет регион (если он используется в другом прайсе)"""
        # Создаем первый прайс
        await authorized_client.post(
            "/price/",
            json={
                "category": "Категория1",
                "supplier": "Поставщик1",
                "region": "ОбщийРегион",
                "price_text": "Текст 1",
            },
        )
        # Создаем второй прайс с тем же регионом
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "Категория2",
                "supplier": "Поставщик2",
                "region": "ОбщийРегион",
                "price_text": "Текст 2",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Удаляем второй прайс
        delete_response = await authorized_client.delete(f"/price/{price_id}")
        assert delete_response.status_code == 200

        # Первый прайс должен остаться
        get_response = await authorized_client.get("/price/?region=общийрегион")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data["data"]["items"]) == 1

    async def test_delete_price_cascade_all(self, authorized_client):
        """Удаление прайса каскадно удаляет связанные записи (category, supplier, region)"""
        # Создаем прайс с уникальными справочниками
        create_response = await authorized_client.post(
            "/price/",
            json={
                "category": "УникальнаяКатегория",
                "supplier": "УникальныйПоставщик",
                "region": "УникальныйРегион",
                "price_text": "Текст прайса",
            },
        )
        price_id = create_response.json()["data"]["id"]

        # Проверяем, что прайс существует
        get_response = await authorized_client.get(f"/price/{price_id}")
        assert get_response.status_code == 200

        # Удаляем прайс
        delete_response = await authorized_client.delete(f"/price/{price_id}")
        assert delete_response.status_code == 200

        # Проверяем, что прайс удален
        get_after_delete = await authorized_client.get(f"/price/{price_id}")
        assert get_after_delete.status_code == 404
