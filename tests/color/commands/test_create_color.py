import pytest



@pytest.mark.asyncio
async def test_create_color_200(authorized_client):

    create_response = await authorized_client.post(
        "/color/",
        json={
            'name': 'красный'
        },
    )
    assert create_response.status_code == 200
